from ta.trend import EMAIndicator, MACD, ADXIndicator, CCIIndicator, PSARIndicator
from ta.momentum import RSIIndicator, StochasticOscillator, WilliamsRIndicator
from ta.volatility import BollingerBands, AverageTrueRange


def calculate_indicators(df):

    close = df["close"]
    high = df["high"]
    low = df["low"]

    # EMA
    ema9 = EMAIndicator(close=close, window=9).ema_indicator().iloc[-1]
    ema21 = EMAIndicator(close=close, window=21).ema_indicator().iloc[-1]
    ema50 = EMAIndicator(close=close, window=50).ema_indicator().iloc[-1]

    # RSI
    rsi = RSIIndicator(close=close, window=14).rsi().iloc[-1]

    # MACD
    macd = MACD(close=close)
    macd_line = macd.macd().iloc[-1]
    signal = macd.macd_signal().iloc[-1]

    # ADX
    adx = ADXIndicator(
        high=high,
        low=low,
        close=close,
        window=14
    ).adx().iloc[-1]

    # Stochastic
    stoch = StochasticOscillator(
        high=high,
        low=low,
        close=close,
        window=14,
        smooth_window=3
    )

    stoch_k = stoch.stoch().iloc[-1]
    stoch_d = stoch.stoch_signal().iloc[-1]

    # Bollinger Bands
    bb = BollingerBands(close=close)

    upper = bb.bollinger_hband().iloc[-1]
    lower = bb.bollinger_lband().iloc[-1]

    # ATR
    atr = AverageTrueRange(
        high=high,
        low=low,
        close=close,
        window=14
    ).average_true_range().iloc[-1]

    # CCI
    cci = CCIIndicator(
        high=high,
        low=low,
        close=close,
        window=20
    ).cci().iloc[-1]

    # Williams %R
    williams = WilliamsRIndicator(
        high=high,
        low=low,
        close=close,
        lbp=14
    ).williams_r().iloc[-1]

    # Parabolic SAR
    psar = PSARIndicator(
        high=high,
        low=low,
        close=close
    ).psar().iloc[-1]

    # Support / Resistance
    support = low.tail(20).min()
    resistance = high.tail(20).max()

    return {

        "price": float(close.iloc[-1]),

        "ema9": float(ema9),
        "ema21": float(ema21),
        "ema50": float(ema50),

        "rsi": float(rsi),

        "macd": float(macd_line),
        "signal": float(signal),

        "adx": float(adx),

        "stoch_k": float(stoch_k),
        "stoch_d": float(stoch_d),

        "upper": float(upper),
        "lower": float(lower),

        "atr": float(atr),

        "cci": float(cci),

        "williams": float(williams),

        "psar": float(psar),

        "support": float(support),
        "resistance": float(resistance)

    }
