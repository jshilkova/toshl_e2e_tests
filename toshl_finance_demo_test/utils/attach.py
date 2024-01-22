import logging

import allure
from allure_commons.types import AttachmentType
import json


def screenshot(browser):
    allure.attach(
        body=browser.driver.get_screenshot_as_png(),
        name='screenshot',
        attachment_type=AttachmentType.PNG,
        extension='.png')


def logs(browser):
    log = "".join(f'{text}\n' for text in browser.driver.get_log(log_type='browser'))
    allure.attach(log, 'browser_logs', AttachmentType.TEXT, '.log')


def html(browser):
    page_html = browser.driver.page_source
    allure.attach(page_html, 'page_source', AttachmentType.HTML, '.html')


def video(browser):
    video_url = "https://selenoid.autotests.cloud/video/" + browser.driver.session_id + ".mp4"
    page_html = "<html><body><video width='100%' height='100%' controls autoplay><source src='" \
                + video_url \
                + "' type='video/mp4'></video></body></html>"
    allure.attach(page_html, 'video_' + browser.driver.session_id, AttachmentType.HTML, '.html')


def screen_xml_dump(browser):
    allure.attach(
        body=browser.driver.page_source,
        name='screen xml dump',
        attachment_type=allure.attachment_type.XML,
    )


def bstack_video(session_id, bs_username, bs_password):
    import requests
    bstack_session = requests.get(
        f'https://api.browserstack.com/app-automate/sessions/{session_id}.json',
        auth=(bs_username, bs_password),
    ).json()
    video_url = bstack_session['automation_session']['video_url']

    allure.attach(
        '<html><body>'
        '<video width="100%" height="100%" controls autoplay>'
        f'<source src="{video_url}" type="video/mp4">'
        '</video>'
        '</body></html>',
        name='video recording',
        attachment_type=allure.attachment_type.HTML,
    )


def as_pretty_json(data):
    if not data:
        return None
    try:
        return json.dumps(json.loads(data), indent=4, ensure_ascii=True)
    except json.JSONDecodeError:
        return None


def attach_request_and_response_data(r, *args, **kwargs):
    allure.attach(
        name="Request url",
        body=r.request.url,
        attachment_type=AttachmentType.TEXT)
    allure.attach(
        name="Request headers",
        body=str(r.request.headers),
        attachment_type=AttachmentType.TEXT)
    request_body = as_pretty_json(r.request.body)
    if request_body:
        allure.attach(
            name="Request body",
            body=request_body,
            attachment_type=AttachmentType.JSON,
            extension="json")
    allure.attach(
        name='Response status code',
        body=str(r.status_code),
        attachment_type=allure.attachment_type.TEXT,
        extension='txt'
    )
    response_body = as_pretty_json(r.text)
    if response_body:
        allure.attach(
            name="Response body",
            body=response_body,
            attachment_type=AttachmentType.JSON,
            extension="json")


def log_request_and_response_data_to_console(r, *args, **kwargs):
    logging.info("Request: " + r.request.url)
    request_body = as_pretty_json(r.request.body)
    if request_body:
        logging.info("INFO Request body: " + request_body)
    logging.info("Request headers: " + str(r.request.headers))
    logging.info("Response code " + str(r.status_code))
    response_body = as_pretty_json(r.text)
    if response_body:
        logging.info("Response: " + response_body)
