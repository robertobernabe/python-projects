#!/usr/bin/python
__author__ = 'robertobernabe'

from HTMLParser import HTMLParser
import argparse
import re
import os
import urllib2
import tempfile
import logging
import sys

from mixcloud_api import MixCloudApi

log = logging.getLogger(__name__)


class MixCloudHtmlParser(HTMLParser):
    def __init__(self, uriCondition):
        HTMLParser.__init__(self)
        self.uriCondition = uriCondition
        self.previewUrl = None
        self.title = None

    def handle_starttag(self, tag, attrs):
        foundTitleContent = False
        if tag == "meta":
            for key, value in attrs:
                if foundTitleContent:
                    self.title = value
                if key == 'property' and value == 'og:title':
                    foundTitleContent = True
        if tag == "span":
            _ = {}
            for key, value in attrs:
                _.setdefault(key, value)

            if 'data-url' and 'data-preview-url' in _.keys():
                if _['data-url'] == self.uriCondition:
                    self.previewUrl = _['data-preview-url']


class MixCloudUrl(object):
    BASE_URI = 'mixcloud.com'

    def __init__(self, url):
        self.url = url

    @property
    def uri(self):
        if self.url.startswith('http://www.'):
            return self.url.split("http://www.%s" % self.BASE_URI)[1]
        else:
            return self.url.split('http://%s' % self.BASE_URI)[1]


class MixCloud(object):
    URL_REGEX_PATTERN = re.compile('http://stream[1-99][0-99]*')

    def __init__(self, url):
        self.mixCloudUrl = MixCloudUrl(url)
        self.mixCloudApi = MixCloudApi(url)
        self.title = None
        self.previewUrl = None
        self._htmlContentFilePath = None

    @property
    def cloudCastFileName(self):
        return self.title.lower().replace(' ', '_')

    @property
    def htmlContentFilePath(self):
        if not self._htmlContentFilePath:
            self._download_website_content()
        return self._htmlContentFilePath

    @property
    def uri(self):
        return self.mixCloudUrl.uri

    def get_download_url(self):
        self._download_website_content()
        self._parse_html_content_file()
        urls = self.generate_download_urls()
        return self.find_valid_download_url(urls)

    def _download(self, url, fileName):
        fileSizeDownloaded = 0
        with open(fileName, mode="wb") as fileDownload:
            ret = urllib2.urlopen(url)
            meta = ret.info()
            fileSize = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s" % (fileName)
            while True:
                data = ret.read(1024)
                fileSizeDownloaded += len(data)
                sys.stdout.write(
                    "\r%s of %s KBytes" % (
                        (fileSizeDownloaded / 1024), (fileSize / 1024)))
                sys.stdout.flush()
                if not data:
                    break
                fileDownload.write(data)
        sys.stdout.write("\n")

    def download(self):
        self._download_website_content()
        self._parse_html_content_file()
        self.download_cloudcast_cover()
        self.download_cloudcast_mp3()

    def download_cloudcast_mp3(self):
        urls = self.generate_download_urls()
        downloadUrl = self.find_valid_download_url(urls)
        fileName = "%s.mp3" % self.cloudCastFileName
        self._download(downloadUrl, fileName)
        self.cloudCastFileNamePath = os.path.abspath(fileName)

    def download_cloudcast_cover(self):
        self._download(
            self.mixCloudApi.picture_url, '%s.jpg' % self.cloudCastFileName)

    def set_mp3_tags(self):
        pass

    def _download_website_content(self):
        log.info("trying to get web content for %s" % self.mixCloudUrl.url)
        response = urllib2.urlopen(self.mixCloudUrl.url)
        encoding = response.headers.getparam('charset')
        html = response.read().decode(encoding)
        _tempFile = tempfile.NamedTemporaryFile(
            prefix='mixcloud-downloader_', delete=False)
        _tempFile.write(html.encode(encoding))
        _tempFile.flush()
        self._htmlContentFilePath = os.path.abspath(_tempFile.name)

    def _parse_html_content_file(self):
        parser = MixCloudHtmlParser(self.mixCloudUrl.uri)
        data = open(self.htmlContentFilePath, 'r').read()
        parser.feed(data.decode('utf-8'))
        self.title = parser.title
        self.previewUrl = parser.previewUrl

    def generate_download_urls(self):
        baseUrl = self.previewUrl.replace(
            '/previews/', '/cloudcasts/originals/')
        match = self.URL_REGEX_PATTERN.match(self.previewUrl)
        downloadUrls = []
        for _ in xrange(1, 100):
            downloadUrl = baseUrl.replace(
                baseUrl[0:match.span()[1]], 'http://stream%s' % _)
            downloadUrls.append(downloadUrl)
        return downloadUrls

    def find_valid_download_url(self, urls):
        for url in urls:
            try:
                ret = urllib2.urlopen(url)
                if ret.code == 200:
                    return url
            except:
                pass

if __name__ == '__main__':

    parser = argparse.ArgumentParser("mixclouddownloader")
    parser.add_argument(
        "cloudcastUrl", action="store",
        help="cloudcast http url http://www.mixcloud.com/...")
    parsedArgs = parser.parse_args()

    url = parsedArgs.cloudcastUrl

    mixCloud = MixCloud(url)
    print mixCloud.mixCloudApi.description
    print mixCloud.mixCloudApi.get_tracklist_printout()
    mixCloud.download()
