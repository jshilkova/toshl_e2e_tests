from typing import Union
import pydantic
import pydantic_settings
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from toshl_finance_demo.data.context import Context
from toshl_finance_demo.utils import file_path


class Common(pydantic_settings.BaseSettings):
    timeout: float
    remote_url: str
    app: str
    appWaitActivity: str = Field(alias='APP_WAIT_ACTIVITY')

    def to_driver_options(self):
        driver_options = UiAutomator2Options()
        driver_options.set_capability('remote_url', self.remote_url)
        driver_options.set_capability('appWaitActivity', self.appWaitActivity)
        return driver_options


class LocalSettings(Common):
    udid: str

    def to_driver_options(self):
        driver_options = super().to_driver_options()
        driver_options.set_capability('udid', self.udid)
        driver_options.set_capability('app', str(file_path.abs_path_from_project(self.app)))
        #        driver_options.set_capability('noReset', True)
        return driver_options


class BstackOptions(pydantic.BaseModel):
    project_name: str
    build_name: str
    session_name: str
    bs_username: str
    bs_password: str

    def as_dict(self):
        return {
            'projectName': self.project_name,
            'buildName': self.build_name,
            'sessionName': self.session_name,
            'userName': self.bs_username,
            'accessKey': self.bs_password,
            'appiumVersion': '2.0.1'
        }


class BstackSettings(Common):
    model_config = SettingsConfigDict(env_nested_delimiter='__')

    platform_name: str
    platform_version: str
    device_name: str
    options: BstackOptions

    def to_driver_options(self):
        driver_options = super().to_driver_options()
        driver_options.set_capability('platformName', self.platform_name)
        driver_options.set_capability('platformVersion', self.platform_version)
        driver_options.set_capability('deviceName', self.device_name)
        driver_options.set_capability('app', self.app)
        driver_options.set_capability('bstack:options', self.options.as_dict())
        return driver_options


def load_config(context):
    _setup = {
        Context.LOCAL: LocalSettings,
        Context.CLOUD: BstackSettings
    }

    def to_dotenv_file_name(ctx):
        if ctx == Context.CLOUD:
            return '.env.bstack'
        elif ctx == Context.LOCAL:
            return f'.env.local_emulator'
        else:
            raise ValueError(f'Unknown context: {ctx}')

    if not load_dotenv(dotenv_path=str(file_path.abs_path_from_project(to_dotenv_file_name(context)))):
        raise Exception('Failed to load environment')
    config: Union[LocalSettings, BstackSettings] = _setup[context]()
    return config
