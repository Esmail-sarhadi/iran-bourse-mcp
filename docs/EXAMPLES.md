# Real examples

_Captured live on 2026-11-04 08:11 UTC. Long responses are trimmed to 46 lines. Latest session in these samples: 2026-11-04. Prices and values are in Rial._

Every response is plain JSON. Keys named `estimate`/`estimated` are derived by the server; everything else is exchange data. Parameter details are in [TOOLS.md](TOOLS.md).

## Market

### `market_status`

```python
market_status()
```

```json
{
  "tehran_time": "2026-11-04 11:41:57",
  "tehran_jdate": "1405/08/13",
  "weekday": "Wednesday",
  "is_trading_weekday": true,
  "within_session_hours": true,
  "session": "Saturday-Wednesday 09:00-12:30 Asia/Tehran (public holidays are not modelled)",
  "bourse": {
    "market_state": "باز",
    "market_state_code": "S",
    "as_of": {
      "date": "2026-11-04",
      "time": "11:41:35"
    },
    "index": {
      "value": 7909908.72,
      "change": 85305.33,
      "change_pct": 1.09
    },
    "equal_weight_index": {
      "value": 2229084.61,
      "change": 14248.8
    },
    "trades": 668149,
    "volume": 30787104981,
    "value": 260869327593060,
    "market_cap": 229121842260007232,
    "units": "rial"
  },
  "gateway": [
    {
      "market": "بورس",
      "open_time": "9:00",
      "close_time": "12:30",
      "is_open": true
    },
    {
      "market": "فرابورس",
      "open_time": "9:00",
      "close_time": "12:30",
      "is_open": true
    }
  ],
  "exchange_server_time": "11/04/2026 08:11:59"
}
```

### `market_overview`

```python
market_overview(market="bourse")
```

```json
{
  "market": "bourse",
  "market_state": "باز",
  "market_state_code": "S",
  "as_of": {
    "date": "2026-11-04",
    "time": "11:41:35"
  },
  "index": {
    "value": 7909908.72,
    "change": 85305.33,
    "change_pct": 1.09
  },
  "equal_weight_index": {
    "value": 2229084.61,
    "change": 14248.8
  },
  "trades": 668149,
  "volume": 30787104981,
  "value": 260869327593060,
  "market_cap": 229121842260007232,
  "units": "rial"
}
```

### `indices`

```python
indices(market="bourse", only_headline=True)
```

```json
{
  "market": "bourse",
  "headline_indices": [
    {
      "name": "شاخص 30 شرکت بزرگ",
      "code": null,
      "headline": true,
      "ins_code": "10523825119011581",
      "value": 552293.58,
      "change": 5626.93,
      "change_pct": 1.0293,
      "high": 555087.12,
      "low": 549850.6,
      "time": "11:41:00"
    },
    {
      "name": "شاخص آزاد شناور",
      "code": null,
      "headline": true,
      "ins_code": "49579049405614711",
      "value": 9856631.19,
      "change": 92850.96,
      "change_pct": 0.951,
      "high": 9880959.95,
      "low": 9817377.24,
      "time": "11:40:00"
    },
    {
      "name": "شاخص بازار اول",
      "code": null,
      "headline": true,
      "ins_code": "62752761908615603",
      "value": 6471900.08,
      "change": 65613.92,
      "change_pct": 1.0242,
      "high": 6486312.13,
      "low": 6444105.49,
      "time": "11:40:00"
    },
    {
      "name": "شاخص بازار دوم",
      "code": null,
      "headline": true,
      "ins_code": "71704845530629737",
      "value": 13815637.3,
      "change": 173670.9,
  … (92 more lines)
```

### `market_watch`

```python
market_watch(sort_by="value", limit=3)
```

```json
{
  "total_instruments": 596,
  "matched": 596,
  "returned": 3,
  "sorted_by": "value",
  "rows": [
    {
      "symbol": "فملی",
      "name": "ملی‌ صنایع‌ مس‌ ایران‌",
      "last": 29170.0,
      "last_pct": 2.97,
      "close": 29080.0,
      "close_pct": 2.65,
      "volume": 898017266,
      "value": 26116778909340,
      "trades": 48553,
      "pe": 14.03,
      "market_cap": 42004800000000000,
      "at_upper_limit": true,
      "at_lower_limit": false,
      "industry": "فلزات اساسی"
    },
    {
      "symbol": "شبندر",
      "name": "پالایش نفت بندرعباس",
      "last": 12470.0,
      "last_pct": -2.12,
      "close": 12390.0,
      "close_pct": -2.75,
      "volume": 867171693,
      "value": 10747483599480,
      "trades": 32007,
      "pe": 2.88,
      "market_cap": 5109493490387000,
      "at_upper_limit": false,
      "at_lower_limit": false,
      "industry": "فراورده های نفتی، کک و سوخت هسته ای"
    },
    {
      "symbol": "فولاد",
      "name": "فولاد مبارکه اصفهان",
      "last": 4330.0,
      "last_pct": 2.85,
      "close": 4290.0,
      "close_pct": 1.9,
      "volume": 1261872847,
  … (11 more lines)
```

### `top_movers`

```python
top_movers(kind="buy_queue", limit=3)
```

```json
{
  "kind": "buy_queue",
  "count": 3,
  "rows": [
    {
      "symbol": "تابان",
      "name": "گروه پتروشیمی تابان فردا",
      "last": 23280.0,
      "last_pct": 2.96,
      "close": 23280.0,
      "close_pct": 2.96,
      "volume": 77064494,
      "value": 1794061420320,
      "trades": 3097,
      "pe": 25.64,
      "market_cap": 6984000000000000,
      "at_upper_limit": true,
      "at_lower_limit": false,
      "industry": "محصولات شیمیایی",
      "queue_volume": 482963107,
      "queue_orders": 6716,
      "queue_value": 11243381130960
    },
    {
      "symbol": "کرماشا",
      "name": "صنایع پتروشیمی کرمانشاه",
      "last": 28380.0,
      "last_pct": 2.98,
      "close": 28380.0,
      "close_pct": 2.98,
      "volume": 40174094,
      "value": 1140140787720,
      "trades": 928,
      "pe": 6.13,
      "market_cap": 592937323440000,
      "at_upper_limit": true,
      "at_lower_limit": false,
      "industry": "محصولات شیمیایی",
      "queue_volume": 194540434,
      "queue_orders": 2220,
      "queue_value": 5521057516920
    },
    {
      "symbol": "خراسان",
      "name": "پتروشیمی خراسان",
      "last": 60730.0,
  … (18 more lines)
```

### `industry_summary`

```python
industry_summary()
```

```json
{
  "total_industries": 43,
  "industries": [
    {
      "industry": "فلزات اساسی",
      "symbols": 48,
      "value": 50248172933253,
      "volume": 5124025678,
      "market_cap": 63363042201882731,
      "avg_change_pct": 1.03,
      "cap_weighted_change_pct": 2.64,
      "index_effect": 48386.61,
      "top_gainer": {
        "symbol": "فسبزوار",
        "pct": 3.0
      },
      "top_loser": {
        "symbol": "فغدیر",
        "pct": -2.97
      },
      "in_buy_queue": 4,
      "in_sell_queue": 0
    },
    {
      "industry": "فراورده های نفتی، کک و سوخت هسته ای",
      "symbols": 12,
      "value": 23680073069390,
      "volume": 2055950551,
      "market_cap": 24421775730177000,
      "avg_change_pct": 1.1,
      "cap_weighted_change_pct": 0.4,
      "index_effect": -3340.18,
      "top_gainer": {
        "symbol": "شبهرن",
        "pct": 3.0
      },
      "top_loser": {
        "symbol": "شپاس",
        "pct": -2.56
      },
      "in_buy_queue": 2,
      "in_sell_queue": 0
    },
    {
      "industry": "محصولات شیمیایی",
      "symbols": 55,
  … (260 more lines)
```

### `index_contributors`

```python
index_contributors(limit=3)
```

```json
{
  "positive": [
    {
      "symbol": "فملی",
      "effect_on_index": 37196.91,
      "last_pct": 2.97,
      "industry": "فلزات اساسی"
    },
    {
      "symbol": "تابان",
      "effect_on_index": 6922.76,
      "last_pct": 2.96,
      "industry": "محصولات شیمیایی"
    },
    {
      "symbol": "فولاد",
      "effect_on_index": 5331.56,
      "last_pct": 2.85,
      "industry": "فلزات اساسی"
    }
  ],
  "negative": [
    {
      "symbol": "فارس",
      "effect_on_index": -16790.27,
      "last_pct": -2.06,
      "industry": "محصولات شیمیایی"
    },
    {
      "symbol": "شپنا",
      "effect_on_index": -5616.76,
      "last_pct": -0.76,
      "industry": "فراورده های نفتی، کک و سوخت هسته ای"
    },
    {
      "symbol": "شبندر",
      "effect_on_index": -4939.27,
      "last_pct": -2.12,
      "industry": "فراورده های نفتی، کک و سوخت هسته ای"
    }
  ],
  "unit": "index points"
}
```

### `market_snapshot`

```python
market_snapshot(date="2026-11-02", limit=3)
```

```json
{
  "date": "2026-11-02",
  "jdate": "1405/08/11",
  "traded_instruments": 2268,
  "rows": [
    {
      "symbol": "اراد2794",
      "name": "مرابحه عام دولت279-ش.خ080218",
      "close": 766148.0,
      "last": 754310.0,
      "yesterday": 770400.0,
      "change_pct": -0.55,
      "open": 775558.0,
      "high": 775558.0,
      "low": 754310.0,
      "volume": 172432102,
      "value": 132108598882916,
      "trades": 3,
      "instrument_id": "IRB4O1860824"
    },
    {
      "symbol": "اراد2524",
      "name": "مرابحه عام دولت252-ش.خ070905",
      "close": 784209.0,
      "last": 784620.0,
      "yesterday": 794200.0,
      "change_pct": -1.26,
      "open": 782072.0,
      "high": 784620.0,
      "low": 782072.0,
      "volume": 142199125,
      "value": 111513867105500,
      "trades": 4,
      "instrument_id": "IRB4O1550794"
    },
    {
      "symbol": "اراد2324",
      "name": "مرابحه عام دولت232-ش.خ070725",
      "close": 793447.0,
      "last": 793610.0,
      "yesterday": 855320.0,
      "change_pct": -7.23,
      "open": 791680.0,
      "high": 793610.0,
      "low": 791680.0,
      "volume": 131466764,
  … (7 more lines)
```

### `market_holder_moves`

```python
market_holder_moves(limit=3)
```

```json
{
  "dates": [
    "2026-10-31",
    "2026-11-01",
    "2026-11-02",
    "2026-11-03",
    "2026-11-04"
  ],
  "moves": [
    {
      "holder": "ETFکدرزروصندوقهای سرمایه گذاری قابل معامله",
      "instrument": "صندوق س. کالای پارسیان",
      "shares_first_day": 53099955,
      "shares_last_day": 853999550,
      "change": 800899595,
      "change_pct": 1508.29
    },
    {
      "holder": "شرکت بیمه ما-سهامی عام -",
      "instrument": "صندوق س. کالای پارسیان",
      "shares_first_day": 14876466,
      "shares_last_day": 148968915,
      "change": 134092449,
      "change_pct": 901.37
    },
    {
      "holder": "BFMصندوق .س .ا.بازارگردانی امیدلوتوس پارسیان",
      "instrument": "صندوق س. کالای پارسیان",
      "shares_first_day": 21412323,
      "shares_last_day": 214234230,
      "change": 192821907,
      "change_pct": 900.52
    }
  ],
  "total_moves": 1128,
  "note": "Large holders whose position in an instrument changed over the last 5 reported days."
}
```

### `supervisor_messages`

```python
supervisor_messages(limit=2)
```

```json
{
  "scope": {
    "market": "bourse"
  },
  "messages": [
    {
      "date": "2026-11-02",
      "jdate": "1405/08/11",
      "time": "14:00:00",
      "title": "اطلاعیه مهم 2",
      "text": "به اطلاع می رساند، پیرو دستور سازمان بورس و اوراق بهادار، ارائه خدمات به ذی‌نفعان بازار سرمایه از طریق وب‌سایت قدیمی TSETMC به نشانی old.tsetmc.com به زودی متوقف خواهد شد. از این رو، خواهشمند است به‌منظور تدوام بهره مندی از خدمات سامانه، در اسرع وقت نسبت به انتقال فیلترهای سفارشی خود به وب سایت اصلی به نشانی www.tsetmc.com اقدام نموده و در صورت نیاز، تغییرات و تنظیمات لازم را برای انطباق فیلترها با ساختار و امکانات سامانه جدید اعمال فرمایید.",
      "truncated": false
    },
    {
      "date": "2026-01-11",
      "jdate": "1404/10/21",
      "time": "10:15:00",
      "title": "اطلاعیه مهم",
      "text": "به آگاهی می رساند در صورت عدم دسترسی به سایت www.tsetmc.com، از آدرس جایگزین www.tsetmc.ir استفاده فرمایید .همچنین در صورت عدم دسترسی به سایت قدیمی old.tsetmc.com ، از آدرس جایگزین old.tsetmc.ir استفاده فرمایید .",
      "truncated": false
    }
  ]
}
```

## Symbol

### `search_symbol`

```python
search_symbol(query="فولاد", limit=3)
```

```json
{
  "query": "فولاد",
  "count": 3,
  "results": [
    {
      "symbol": "فولاد",
      "name": "فولاد مبارکه اصفهان",
      "ins_code": "46348559193224090",
      "market": "bourse",
      "board": "N1"
    },
    {
      "symbol": "توسکا",
      "name": "صندوق س توسعه فولاد- ثابت",
      "ins_code": "56871139881800017",
      "market": "bourse",
      "board": "بازار صندوق های قابل معامله"
    },
    {
      "symbol": "حدید",
      "name": "صندوق صنایع گنجینه فولاد1-بخشی",
      "ins_code": "25422370845365439",
      "market": "bourse",
      "board": "بازار صندوق های قابل معامله"
    }
  ]
}
```

### `symbol_overview`

```python
symbol_overview(symbol="فولاد")
```

```json
{
  "identity": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "name_en": "S*Mobarakeh Steel",
    "ins_code": "46348559193224090",
    "isin": "IRO1FOLD0009",
    "instrument_id": "IRO1FOLD0001",
    "market": "بازار بورس",
    "board": "بازار اول (تابلوی اصلی) بورس",
    "sector": "فلزات اساسی",
    "sector_code": "27",
    "sub_sector": "تولید آهن و فولاد پایه",
    "instrument_kind": "stock"
  },
  "quote": {
    "date": "2026-11-04",
    "jdate": "1405/08/13",
    "last_update": "11:41:46",
    "status": {
      "code": "A",
      "title": "مجاز",
      "under_supervision": 0
    },
    "last": {
      "price": 4330.0,
      "change": 120.0,
      "change_pct": 2.85
    },
    "close": {
      "price": 4290.0,
      "change": 80.0,
      "change_pct": 1.9
    },
    "yesterday_close": 4210.0,
    "open": 4240.0,
    "high": 4330.0,
    "low": 4140.0,
    "volume": 1263190160,
    "value": 5416395225900,
    "trades": 15336,
    "vwap": 4287.87,
    "price_limits": {
      "upper": 4330.0,
      "lower": 4090.0
    },
  … (346 more lines)
```

### `quote`

```python
quote(symbol="فولاد")
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "date": "2026-11-04",
  "jdate": "1405/08/13",
  "last_update": "11:41:46",
  "status": {
    "code": "A",
    "title": "مجاز",
    "under_supervision": 0
  },
  "last": {
    "price": 4330.0,
    "change": 120.0,
    "change_pct": 2.85
  },
  "close": {
    "price": 4290.0,
    "change": 80.0,
    "change_pct": 1.9
  },
  "yesterday_close": 4210.0,
  "open": 4240.0,
  "high": 4330.0,
  "low": 4140.0,
  "volume": 1263190160,
  "value": 5416395225900,
  "trades": 15336,
  "vwap": 4287.87,
  "price_limits": {
    "upper": 4330.0,
    "lower": 4090.0
  },
  "at_upper_limit": true,
  "at_lower_limit": false,
  "ranges": {
    "week": {
      "low": 4020.0,
      "high": 4210.0
    },
    "year": {
      "low": 2182.0,
  … (16 more lines)
```

### `order_book`

```python
order_book(symbol="فولاد")
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "as_of": {
    "date": "2026-11-04",
    "last_trade_time": "11:41:46"
  },
  "bids": [
    {
      "level": 1,
      "price": 4330.0,
      "volume": 595743071,
      "orders": 2428
    },
    {
      "level": 2,
      "price": 4320.0,
      "volume": 2971985,
      "orders": 27
    },
    {
      "level": 3,
      "price": 4310.0,
      "volume": 381569,
      "orders": 4
    },
    {
      "level": 4,
      "price": 4300.0,
      "volume": 2382979,
      "orders": 29
    },
    {
      "level": 5,
      "price": 4290.0,
      "volume": 4071788,
      "orders": 27
    }
  ],
  "asks": [
    {
      "level": 1,
  … (50 more lines)
```

### `order_book_history`

```python
order_book_history(symbol="فولاد", date="2026-11-02", step_seconds=3600)
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "date": "2026-11-02",
  "jdate": "1405/08/11",
  "total_events": 13780,
  "events_span": {
    "first": "06:01:28",
    "last": "14:15:30",
    "covers_full_session": true
  },
  "warning": null,
  "price_limits": {
    "upper": 4240.0,
    "lower": 4000.0
  },
  "window": {
    "from": "08:30:00",
    "to": "12:35:00"
  },
  "snapshots_in_range": 13722,
  "samples": [
    {
      "time": "08:45:00",
      "best_bid": 4000.0,
      "best_ask": 4000.0,
      "bid_volume": 453225,
      "ask_volume": 662000,
      "imbalance": -0.1872,
      "queue": null,
      "queue_volume": 0
    },
    {
      "time": "09:00:00",
      "best_bid": 4050.0,
      "best_ask": 4050.0,
      "bid_volume": 34867117,
      "ask_volume": 20791861,
      "imbalance": 0.2529,
      "queue": null,
      "queue_volume": 0
    },
  … (36 more lines)
```

### `trades`

```python
trades(symbol="فولاد", date="2026-11-02", min_volume=250000, limit=3)
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "date": "2026-11-02",
  "jdate": "1405/08/11",
  "matched": 742,
  "returned": 3,
  "truncated": true,
  "trades": [
    {
      "n": 1,
      "time": "09:00:12",
      "price": 4080.0,
      "volume": 300000,
      "value": 1224000000
    },
    {
      "n": 2,
      "time": "09:00:12",
      "price": 4080.0,
      "volume": 300000,
      "value": 1224000000
    },
    {
      "n": 3,
      "time": "09:00:12",
      "price": 4080.0,
      "volume": 300000,
      "value": 1224000000
    }
  ],
  "units": "price/value in rial, volume in shares"
}
```

### `trade_summary`

```python
trade_summary(symbol="فولاد", date="2026-11-02", interval_minutes=30)
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "date": "2026-11-02",
  "jdate": "1405/08/11",
  "summary": {
    "ticks": 15643,
    "cancelled_ticks": 0,
    "first_trade": "09:00:12",
    "last_trade": "12:30:00",
    "volume": 980098090,
    "value": 4010393789380,
    "vwap": 4091.83,
    "open": 4080.0,
    "high": 4160.0,
    "low": 4020.0,
    "close": 4130.0,
    "avg_trade_volume": 62654,
    "median_trade_volume": 20000
  },
  "completeness": {
    "ticks_volume": 980098090,
    "ticks_count": 15643,
    "official_volume": 980098090,
    "volume_coverage_pct": 100.0,
    "official_trade_count": 15643,
    "count_coverage_pct": 100.0,
    "note": "Coverage compares tick data with the exchange's own daily totals; ~100% means nothing is missing."
  },
  "bars": [
    {
      "from": "09:00",
      "open": 4080.0,
      "high": 4160.0,
      "low": 4020.0,
      "close": 4040.0,
      "volume": 273025606,
      "value": 1110127706200,
      "trades": 4177,
      "vwap": 4066.02
    },
    {
  … (201 more lines)
```

### `price_history`

```python
price_history(symbol="فولاد", limit=3, adjusted=True)
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "adjusted": true,
  "adjustment_events": [
    {
      "date": "2009-06-23",
      "jdate": "1388/04/02",
      "factor": 0.717248
    },
    {
      "date": "2010-07-07",
      "jdate": "1389/04/16",
      "factor": 0.793046
    },
    {
      "date": "2011-02-14",
      "jdate": "1389/11/25",
      "factor": 0.706881
    },
    {
      "date": "2011-07-20",
      "jdate": "1390/04/29",
      "factor": 0.900925
    },
    {
      "date": "2012-07-29",
      "jdate": "1391/05/08",
      "factor": 0.876238
    },
    {
      "date": "2013-07-22",
      "jdate": "1392/04/31",
      "factor": 0.869974
    },
    {
      "date": "2013-07-27",
      "jdate": "1392/05/05",
      "factor": 0.743389
    },
    {
      "date": "2014-07-21",
  … (160 more lines)
```

### `real_legal_flow`

```python
real_legal_flow(symbol="فولاد", days=3)
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "latest_session": {
    "date": "2026-11-04",
    "real": {
      "buy": {
        "volume": 812229008,
        "count": 2272,
        "value": 3482732418742,
        "value_estimated": true,
        "avg_per_participant": 1532892789.94,
        "avg_volume_per_participant": 357495.16
      },
      "sell": {
        "volume": 1072458633,
        "count": 3596,
        "value": 4598563228007,
        "value_estimated": true,
        "avg_per_participant": 1278799562.85,
        "avg_volume_per_participant": 298236.55
      },
      "net_volume": -260229625,
      "net_value": -1115830809265
    },
    "legal": {
      "buy": {
        "volume": 450956152,
        "count": 33,
        "value": 1933641367807,
        "value_estimated": true,
        "avg_per_participant": 58595192963.86,
        "avg_volume_per_participant": 13665337.94
      },
      "sell": {
        "volume": 190726527,
        "count": 24,
        "value": 817810558542,
        "value_estimated": true,
        "avg_per_participant": 34075439939.28,
        "avg_volume_per_participant": 7946938.62
      },
  … (54 more lines)
```

### `shareholders`

```python
shareholders(symbol="فولاد")
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "shares_outstanding": 1935000000000,
  "listed_holders": 12,
  "listed_percent_total": 46.48,
  "unlisted_percent": 53.52,
  "top5_percent": 35.8,
  "holders": [
    {
      "name": "سازمان توسعه ونوسازی معادن وصنایع معدنی ایران",
      "shares": 323334093547,
      "percent": 16.709,
      "change_amount": 0.0,
      "holder_id": 1241318
    },
    {
      "name": "شرکت توسعه سرمایه رفاه -سهامی خاص -",
      "shares": 203548440651,
      "percent": 10.519,
      "change_amount": 0.0,
      "holder_id": 1245645
    },
    {
      "name": "موسسه صندوق بازنشستگی ،وظیفه ،ازکارافتادگی وپ",
      "shares": 68902471229,
      "percent": 3.56,
      "change_amount": 0.0,
      "holder_id": 1242405
    },
    {
      "name": "موسسه صندوق بیمه اجتماعی روستائیان وعشایر",
      "shares": 51974268209,
      "percent": 2.686,
      "change_amount": 0.0,
      "holder_id": 1245644
    },
    {
      "name": "شرکت سرمایه گذاری صدرتامین -سهامی عام -",
      "shares": 45059916642,
      "percent": 2.328,
      "change_amount": 0.0,
  … (54 more lines)
```

### `shareholder_history`

```python
shareholder_history(symbol="فولاد")
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "snapshots": [
    {
      "date": "2026-11-04",
      "holders": [
        {
          "name": "سازمان توسعه ونوسازی معادن وصنایع معدنی ایران",
          "shares": 323334093547,
          "percent": 16.709,
          "shares_change": null,
          "new_in_list": false
        },
        {
          "name": "شرکت توسعه سرمایه رفاه -سهامی خاص -",
          "shares": 203548440651,
          "percent": 10.519,
          "shares_change": null,
          "new_in_list": false
        },
        {
          "name": "موسسه صندوق بازنشستگی ،وظیفه ،ازکارافتادگی وپ",
          "shares": 68902471229,
          "percent": 3.56,
          "shares_change": null,
          "new_in_list": false
        },
        {
          "name": "موسسه صندوق بیمه اجتماعی روستائیان وعشایر",
          "shares": 51974268209,
          "percent": 2.686,
          "shares_change": null,
          "new_in_list": false
        },
        {
          "name": "شرکت سرمایه گذاری صدرتامین -سهامی عام -",
          "shares": 45059916642,
          "percent": 2.328,
          "shares_change": null,
          "new_in_list": false
        },
  … (54 more lines)
```

### `shareholder_portfolio`

```python
shareholder_portfolio(holder_id="1241318")
```

```json
{
  "holder_id": 1241318,
  "holdings": [
    {
      "symbol": "نی ریز",
      "name": "فولاد غدیر نی ریز",
      "shares": 5249999000,
      "percent": 34.999,
      "change_amount": null
    },
    {
      "symbol": "احیا",
      "name": "احیا استیل فولاد بافت",
      "shares": 12831000000,
      "percent": 20.0,
      "change_amount": null
    },
    {
      "symbol": "فولاد",
      "name": "فولاد مبارکه اصفهان",
      "shares": 323334093547,
      "percent": 16.709,
      "change_amount": null
    },
    {
      "symbol": "فملی",
      "name": "ملی‌ صنایع‌ مس‌ ایران‌",
      "shares": 166328803050,
      "percent": 11.55,
      "change_amount": null
    },
    {
      "symbol": "آلومینا",
      "name": "آلومینای ایران",
      "shares": 100716374,
      "percent": 5.036,
      "change_amount": null
    }
  ]
}
```

### `corporate_actions`

```python
corporate_actions(symbol="فولاد")
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "price_adjustments": [
    {
      "date": "2026-08-03",
      "jdate": "1405/05/12",
      "price_before": 2604.0,
      "price_after": 2549.0,
      "factor": 0.978879
    },
    {
      "date": "2025-08-04",
      "jdate": "1404/05/13",
      "price_before": 2860.0,
      "price_after": 2580.0,
      "factor": 0.902098
    },
    {
      "date": "2024-07-21",
      "jdate": "1403/04/31",
      "price_before": 5200.0,
      "price_after": 4800.0,
      "factor": 0.923077
    },
    {
      "date": "2023-07-22",
      "jdate": "1402/04/31",
      "price_before": 5460.0,
      "price_after": 4960.0,
      "factor": 0.908425
    },
    {
      "date": "2022-08-03",
      "jdate": "1401/05/12",
      "price_before": 11170.0,
      "price_after": 9470.0,
      "factor": 0.847807
    },
    {
      "date": "2021-08-03",
      "jdate": "1400/05/12",
  … (211 more lines)
```

### `symbol_statistics`

```python
symbol_statistics(symbol="فولاد")
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "metrics": [
    {
      "metric": "میانگین ارزش معاملات در 3 ماه گذشته",
      "value": 11496274310831.0,
      "code": 1
    },
    {
      "metric": "میانگین ارزش معاملات در 12 ماه گذشته",
      "value": 3992178323327.0,
      "code": 2
    },
    {
      "metric": "رتبه ارزش معاملات در 3 ماه گذشته",
      "value": 17.0,
      "code": 3
    },
    {
      "metric": "رتبه ارزش معاملات در 12 ماه گذشته",
      "value": 31.0,
      "code": 4
    },
    {
      "metric": "میانگین حجم معاملات در 3 ماه گذشته",
      "value": 3584561989.0,
      "code": 5
    },
    {
      "metric": "میانگین حجم معاملات در 12 ماه گذشته",
      "value": 1208872869.0,
      "code": 6
    },
    {
      "metric": "رتبه حجم معاملات در 3 ماه گذشته",
      "value": 6.0,
      "code": 7
    },
    {
      "metric": "رتبه حجم معاملات در 12 ماه گذشته",
      "value": 8.0,
  … (404 more lines)
```

### `etf_nav`

```python
etf_nav(symbol="اهرم")
```

```json
{
  "instrument": {
    "symbol": "اهرم",
    "name": "صندوق س سهامی کاریزما- اهرمی",
    "ins_code": "17914401175772326",
    "market": "bourse",
    "board": "بازار صندوق های قابل معامله"
  },
  "available": true,
  "date": "2026-11-04",
  "time": "11:41:01",
  "last_price": 74063.0,
  "nav_redemption": 91661.0,
  "nav_issue": 92958.0,
  "premium_to_redemption_nav_pct": -19.2,
  "premium_to_issue_nav_pct": -20.33,
  "note": "pRedTran / pSubTran are the exchange's redemption (ابطال) and issue (صدور) NAV figures."
}
```

## Codal

### `codal_filings`

```python
codal_filings(symbol="فولاد", limit=2)
```

```json
{
  "total_matches": 1475,
  "pages": 74,
  "page": 1,
  "returned": 2,
  "filings": [
    {
      "tracing_no": 1621524,
      "symbol": "فولاد",
      "company": "فولاد مبارکه اصفهان",
      "title": "گزارش فعالیت ماهانه دوره ۱ ماهه منتهی به ۱۴۰۵/۰۷/۳۰",
      "letter_code": "ن-۳۰",
      "published": "1405/08/06 16:01:48",
      "sent": "1405/08/06 16:01:48",
      "under_supervision": false,
      "is_estimate": false,
      "has": {
        "html": true,
        "pdf": true,
        "excel": true,
        "xbrl": false,
        "attachment": true
      },
      "links": {
        "page": "https://codal.ir/Reports/Decision.aspx?LetterSerial=LyQnlYP7OOObOOOIDLto8TGJDkDQ%3d%3d&rt=0&let=58&ct=0&ft=-1",
        "pdf": "https://codal.ir/DownloadFile.aspx?hs=LyQnlYP7OOObOOOIDLto8TGJDkDQ%3d%3d&ft=1005&let=58",
        "excel": "https://excel.codal.ir/service/Excel/GetAll/LyQnlYP7OOObOOOIDLto8TGJDkDQ%3d%3d/0",
        "attachments": "https://codal.ir/Reports/Attachment.aspx?LetterSerial=LyQnlYP7OOObOOOIDLto8TGJDkDQ%3d%3d"
      }
    },
    {
      "tracing_no": 1618277,
      "symbol": "فولاد",
      "company": "فولاد مبارکه اصفهان",
      "title": "توضیحات در خصوص اطلاعات و صورت های مالی منتشر شده",
      "letter_code": "ن-۲۶",
      "published": "1405/07/30 14:40:53",
      "sent": "1405/07/30 14:40:53",
      "under_supervision": false,
      "is_estimate": false,
      "has": {
        "html": true,
        "pdf": true,
        "excel": false,
        "xbrl": false,
        "attachment": true
  … (11 more lines)
```

### `codal_company`

```python
codal_company(symbol="فولاد")
```

```json
{
  "instrument": {
    "symbol": "فولاد",
    "name": "فولاد مبارکه اصفهان",
    "ins_code": "46348559193224090",
    "market": "bourse"
  },
  "available": true,
  "name": "فولاد مبارکه اصفهان",
  "isic": "271018",
  "ceo": "سعید زرندی",
  "address": "اصفهان کیلومتر 75 جنوب غربی کدپستی 8488111131",
  "phone": "03152733838",
  "fax": "03152733922",
  "activity": "1) بهره برداری از کارخانه فولادسازی مجتمع فولاد مبارکه واقع در 74 کیلومتری شهر اصفهان 2) انجام هرگونه فعالیت تولیدی معاملاتی و بازرگانی اعم از داخلی و خارجی که بطور مستقیم یا غیرمستقیم با موضوع شرکت مرتبط باشد 3) اکتشاف،استخراج و بهره برداری از معادن فلزی و غیر فلزی مورد نیاز صنعت فولاد از جمله استخراج و فرآوری سنگ آهن ، دولومیت و تولید سنگ آهن دانه بندی،کنسانتره و گندله از آن"
}
```

## Help

### `glossary`

```python
glossary(term="صف خرید")
```

```json
{
  "query": "صف خرید",
  "matches": {
    "صف خرید": {
      "en": "buy queue",
      "meaning": "The price is locked at the daily upper limit and nobody offers shares for sale; buyers queue up. The queue size is the buy volume waiting at that price."
    }
  },
  "hint": null
}
```
