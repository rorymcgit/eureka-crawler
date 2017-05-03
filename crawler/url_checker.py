
class URLChecker:

    def url_is_valid(self, url):
        return self.url_is_http(url) and self.url_domain_is_good(url) and not self.is_low_quality_link(url)

    def url_is_http(self, url):
        return url.startswith('http')

    def url_domain_is_good(self, url):
        return '.co.uk' in url or '.com' in url or '.org' in url

    def is_low_quality_link(self, url):
        low_quality_links = ['plus.google.com',
                            'accounts.google.com',
                            'facebook.com',
                            'twitter.com',
                            'apple.com',
                            'instagram.com',
                            'download-sha1',
                            'download.mozilla',
                            'donate.mozilla',
                            'wikipedia.org'
                            'bugzilla']
        return True if any(bad_link in url for bad_link in low_quality_links) else False
