__author__ = 'fschaeffeler'
import urllib2
import json


class MixCloudApi(object):
    API_BASE_URI = "http://api.mixcloud.com"
    WWW_BASE_URI = "http://www.mixcloud.com"

    def __init__(self, cloudcastUrl):
        self.cloudcastUrl = cloudcastUrl
        self._cloudcast = None

    @property
    def cloudcastApiUrl(self):
        if not self.API_BASE_URI in self.cloudcastUrl:
            if self.WWW_BASE_URI in self.cloudcastUrl:
                return self.cloudcastUrl.replace(
                    self.WWW_BASE_URI, self.API_BASE_URI)
        else:
            return self.cloudcastUrl

    @property
    def cloudcast(self):
        if not self._cloudcast:
            self._cloudcast = json.load(urllib2.urlopen(self.cloudcastApiUrl))
        return self._cloudcast

    @property
    def name(self):
        return self.cloudcast['name']

    @property
    def description(self):
        return self.cloudcast['description']

    @property
    def tracklist(self):
        tracks = []
        for track in self.cloudcast['sections']:
            tracks.append(
                (track['track']['artist']['name'].encode('utf-8'),
                 track['track']['name'].encode('utf-8'), track['start_time']))
        return tracks

    @property
    def picture_url(self):
        return self.cloudcast['pictures']['large']

    def get_tracklist_printout(self):
        str_format = "%s - %s (%s:%s:%s)"
        printout = ""
        for item in self.tracklist:
            printout = printout + str_format % (
                item[0], item[1],
                item[2] / 3600, item[2] / 60, item[2] % 60) + "\n"
        return printout


if __name__ == '__main__':
    api = MixCloudApi("http://www.mixcloud.com/DJ_Vaya/calientemente-yours-the-mixtape-vol-1/")
    print api.name
    print api.picture_url
    print api.get_tracklist_printout()