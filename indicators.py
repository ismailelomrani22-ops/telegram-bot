from ta.trend import (
    EMAIndicator,
    MACD,
    ADXIndicator,
    CCIIndicator,
    PSARIndicator
)

from ta.momentum import (
    RSIIndicator,
    StochasticOscillator,
    WilliamsRIndicator
)

from ta.volatility import (
    BollingerBands,
    AverageTrueRange
)


def calculate_indicators(df):

    close = df["close"]
    high = df["high"]
    low = df["low"]

    # ==========================
    # EMA
    # ==========================

    ema9 = EMAIndicator(close, window=9).ema_indicator().iloc[-1]
    ema21 = EMAIndicator(close, window=21).ema_indicator().iloc[-1]
    ema50 = EMAIndicator(close, window=50).ema_indicator().iloc[-1]
    ema100 = EMAIndicator(close, window=100).ema_indicator().iloc[-1]
    ema200 = EMAIndicator(close, window=200).ema_indicator().iloc[-1]

    # ==========================
    # RSI
    # ==========================

    rsi = RSIIndicator(close, window=14).rsi().iloc[-1]

    # ==========================
    # MACD
    # ==========================

    macd = MACD(close)

    macd_line = macd.macd().iloc[-1]
    signal = macd.macd_signal().iloc[-1]
    histogram = macd.macd_diff().iloc[-1]

    # ==========================
    # ADX
    # ==========================

    adx = ADXIndicator(high, low, close).adx().iloc[-1]

    # ==========================
    # STOCHASTIC
    # ==========================

    stoch = StochasticOscillator(high, low, close)

    stoch_k = stoch.stoch().iloc[-1]
    stoch_d = stoch.stoch_signal().iloc[-1]

    # ==========================
    # BOLLINGER
    # ==========================

    bb = BollingerBands(close)

    upper = bb.bollinger_hband().iloc[-1]
    middle = bb.bollinger_mavg().iloc[-1]
    lower = bb.bollinger_lband().iloc[-1]

    # ==========================
    # ATR
    # ==========================

    atr = AverageTrueRange(high, low, close).average_true_range().iloc[-1]

    # ==========================
    # CCI
    # ==========================

    cci = CCIIndicator(
        high,
        low,
        close,
        window=20
    ).cci().iloc[-1]

    # ==========================
    # Williams %R
    # ==========================

    williams = WilliamsRIndicator(
        high,
        low,
        close,
        lbp=14
    ).williams_r().iloc[-1]

    # ==========================
    # PARABOLIC SAR
    # ==========================

    psar = PSARIndicator(
        high,
        low,
        close
    ).psar().iloc[-1]

    # ==========================
    # SUPPORT / RESISTANCE
    # ==========================

    support = low.tail(50).min()
    resistance = high.tail(50).max()

    return {

        "price": float(close.iloc[-1]),

        "ema9": float(ema9),
        "ema21": float(ema21),
        "ema50": float(ema50),
        "ema100": float(ema100),
        "ema200": float(ema200),

        "rsi": float(rsi),

        "macd": float(macd_line),
        "signal": float(signal),
        "histogram": float(histogram),

        "adx": float(adx),

        "stoch_k": float(stoch_k),
        "stoch_d": float(stoch_d),

        "upper": float(upper),
        "middle": float(middle),
        "lower": float(lower),

        "atr": float(atr),

        "cci": float(cci),

        "williams": float(williams),

        "psar": float(psar),

        "support": float(support),
        "resistance": float(resistance)

    }
