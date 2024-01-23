import requests
from logs import Logger
import config



class JudgementScraper:
    def __init__(self):
        self.logger = Logger("judgement_scraper").log_obj

    
    def get_captcha_value(self, session):
        try:
            captcha_response = session.get(config.CAPTCHA_URL)
            captcha_value = captcha_response.text.strip()
            if captcha_value:
                self.logger.info(f"Captcha value found: {captcha_value}")
                return captcha_value
            else:
                self.logger.error("Captcha value not found.")
                return None
        except requests.RequestException as e:
            self.logger.error(f"Error fetching captcha: {e}")
            return None

    
    def scrape_judgements(self):
        try:
            session = requests.session()
            captcha_value = self.get_captcha_value(session)

            if captcha_value:
                payload = {
                    'nw_hd_fst': 0,
                    'inc_val': 50,
                    'u_t': 1,
                    'JCBfrom_date': config.FROM_DATE,
                    'JCBto_date': config.TO_DATE,
                    'ansCaptcha': captcha_value
                }

                submit_response = session.post(config.CAPTCHA_SUBMIT_URL, data=payload)

                if submit_response.status_code == 200:
                    self.logger.info("Judgments scraped successfully.")
                    return submit_response
                else:
                    self.logger.error(f"Failed to scrape judgments. Status code: {submit_response.status_code}")
            else:
                return None
        except requests.RequestException as e:
            self.logger.error(f"Error scraping judgments: {e}")
            return None


if __name__ == "__main__":
    scraper = JudgementScraper()
    result = scraper.scrape_judgements()

