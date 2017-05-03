class URLSplicer():

    def cut_string(self, url):
        if url.count('/') >= 4:
            string_cut = self.find_nth(url, '/', 3)
            return url[:string_cut]
        else:
            return url

    def find_nth(self, haystack, needle, n):
        parts = haystack.split(needle, n+1)
        if len(parts) <= n+1:
            return -1
        return len(haystack)-len(parts[-1])-len(needle)
