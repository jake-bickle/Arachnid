class AOPICBank:
    def __init__(self, seed, starting_credits=100000):
        self.seed = seed
        self.bank = {seed: starting_credits}
        self.virtual_credit = 0

    def highest_priority_c_url(self):
        # AOPIC modification: Return None if c_url with highest value is 0
        c_url = max(self.bank, key=self.bank.get)
        return c_url if self.bank[c_url] != 0 else None

    def disperse_credits(self, c_url, found_c_urls, is_supplemental=False):
        """ Takes the credits of c_url and disperses them among found_c_urls
        This performs a modified version of the AOPIC algorithm. Refer to the following issue for more info:
        https://github.com/jake-bickle/Arachnid/issues/6
        """
        creds = self.relinquish_credits(c_url, is_supplemental)
        creds = self.tax_credits(creds)
        self.divide_credits_among_c_urls(creds, found_c_urls)
        self.disperse_virtual_credits_if_necessary()

    def relinquish_credits(self, c_url, is_supplemental=False):
        if is_supplemental:
            # AOPIC modification: Any supplemental prev_c_url is given 1000 credits
            creds = 1000
        else:
            creds = self.bank[c_url]
            self.bank[c_url] = 0
        return creds

    def tax_credits(self, creds):
        tax = creds / 10
        self.virtual_credit += tax
        return creds - tax

    def divide_credits_among_c_urls(self, creds, c_urls):
        if len(c_urls) > 0:
            credits_per_page = creds / len(c_urls)
            for c_url in c_urls:
                try:
                    # AOPIC modification: Do not give credit to any c_url with 0 credits
                    if self.bank[c_url] != 0:
                        self.bank[c_url] += credits_per_page
                except KeyError:
                    self.bank[c_url] = credits_per_page

    def disperse_virtual_credits_if_necessary(self):
        pages_to_receive_bonus = self.uncrawled_pages()
        if max(self.bank.values()) < self.virtual_credit and len(pages_to_receive_bonus) != 0:
            bonus = self.virtual_credit / len(pages_to_receive_bonus)
            for c_url in pages_to_receive_bonus:
                self.bank[c_url] += bonus
            self.virtual_credit = 0

    def uncrawled_pages(self):
        uncrawled_pages = list()
        for c_url, creds in self.bank.items():
            if creds > 0:
                uncrawled_pages.append(c_url)
        return uncrawled_pages
