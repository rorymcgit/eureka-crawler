class URLSplicer():

    def cut_url(self, url):
        if url.count('/') >= 4:
            string_cut = self.find_nth(url, '/', 3)
            return url[:string_cut]
        else:
            return url

    def find_nth(self, url, forward_slash, n):
        parts = url.split(forward_slash, n+1)
        if len(parts) <= n+1:
            return -1
        return len(url)-len(parts[-1])-len(forward_slash)
