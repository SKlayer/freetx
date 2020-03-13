from freetx.format import verify_sig
from freetx.network.rates import SUPPORTED_CURRENCIES, set_rate_cache_time
from freetx.network.services import set_service_timeout
from freetx.wallet import Key, PrivateKey, PrivateKeyTestnet, wif_to_key

__version__ = '1.0.0.0'
