
class URLChecker:

    def url_is_valid(self, url):
        return self.check_url_beginning(url) and self.check_url_domain(url) and not self.is_low_quality_link(url)

    def check_url_beginning(self, url):
        return url.startswith('http')

    def check_url_domain(self, url):
        return '.co.uk' in url or '.com' in url or '.org' in url

    def is_low_quality_link(self, url):
        low_quality_links = ['plus.google.com', 'accounts.google.com', 'facebook.com', 'twitter.com', 'apple.com', 'instagram.com', 'download-sha1', 'download.mozilla', 'donate.mozilla', 'bugzilla']
        return True if any(bad_link in url for bad_link in low_quality_links) else False
