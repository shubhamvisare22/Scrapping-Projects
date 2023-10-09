import requests


CAPTCHA_URL = "https://main.sci.gov.in/php/captcha_num.php"
CAPTCHA_SUBMIT_URL = "https://main.sci.gov.in/php/v_judgments/getJCB_new.php"
FROM_DATE = '09-01-2022'
TO_DATE = '27-07-2023'


def scrape_judgements():
    session = requests.session()
    captcha_response = session.get(CAPTCHA_URL)
    captcha_value = captcha_response.text.strip()

    if captcha_value:
        payload = {
            'nw_hd_fst': 0,
            'inc_val': 50,
            'u_t': 1,
            'JCBfrom_date': FROM_DATE,
            'JCBto_date': TO_DATE,
            'ansCaptcha': captcha_value
        }

        submit_response = session.post(CAPTCHA_SUBMIT_URL, data=payload)

        if submit_response.status_code == 200:
            print("Judgments scraped successfully.")
            return submit_response
        else:
            print(
                f"Failed to scrape judgments. Status code: {submit_response.status_code}")
    else:
        print("Captcha value not found.")
        return captcha_response.status_code


if __name__ == "__main__":
    scrape_judgements()
