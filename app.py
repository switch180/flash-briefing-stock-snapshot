from chalice import Chalice, ForbiddenError
from chalicelib.RobinhoodSource import RobinhoodSource
from chalicelib import config
from chalicelib.Heater import Heater
from chalicelib.utils import signature_check

import logging
logger = logging.getLogger('my-app')

app = Chalice(app_name='FlashBriefingStockSkill')
#TODO dynamic debug
app.debug = False
logger.setLevel(logging.DEBUG)
private_path = config.private_path

@app.schedule('rate(5 minutes)')
def heater(event):
    heater = Heater()
    req = heater.heat_warm()
    return {'status': req.status_code}

@app.route('/warm')
def warm():
    init_variables()
    return {'status': 200}

@app.route('/' + private_path + '/{signature}')
@signature_check
def index(signature):
    ar = None
    try:
        ar = get_robinhood_quote()
    except Exception as e:
        logger.error("Robinhood data retreival failed!")
        import traceback
        logger.debug(traceback.print_exc())
        return
    else:
        logger.info(ar)
        return ar.get_resp()

def get_robinhood_quote():
    rh_source = RobinhoodSource(config.stock_symbol, config.stock_friendly_name, r_username, r_password)
    rh_source.set_position(config.avg_price, config.shares_held, config.shares_awarded)
    return rh_source.get_response()
