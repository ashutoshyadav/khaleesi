import json

returns = {
  "ADANIPORTS.NS": {
    "ROE": 13.70,
    "name": "Adani Ports & Special Economic Zone Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Consumer, Non-Cyclical",
    "ROCE": 13.88
  },
  "ASIANPAINT.NS": {
    "ROE": 25.45,
    "name": "Asian Paints Ltd",
    "ROCE": 38.10,
    "sub-sector": "Basic Materials",
    "sector": "NON-FINANCIAL"
  },
  "AXISBANK.NS": {
    "ROE": 0.06,
    "name": "Axis Bank Ltd",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 4.48
  },
  "BAJAJ-AUTO.NS": {
    "ROE": 22.51,
    "name": "Bajaj Auto Ltd",
    "sector": "NON-FINANCIAL",
    "ROCE": 31.54,
    "sub-sector": "Auto"
  },
  "BAJFINANCE.NS": {
    "ROE": 20.27,
    "name": "Bajaj Finance Ltd",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 12.45
  },
  "BAJAJFINSV.NS": {
    "ROE": 5.01,
    "name": "Bajaj Finserv Ltd",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 5.89
  },
  "BHARTIARTL.NS": {
    "ROE": 0.73,
    "name": "Bharti Airtel Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Communications",
    "ROCE": 3.49
  },
  "INFRATEL.NS": {
    "ROE": 14.22,
    "name": "Bharti Infratel Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Communications",
    "ROCE": 18.43
  },
  "BPCL.NS": {
    "ROE": 24.82,
    "name": "Bharat Petroleum Corp Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Energy",
    "ROCE": 21.21
  },
  "CIPLA.NS": {
    "ROE": 10.91,
    "name": "Ciple Ltd/India",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Consumer, Cyclical",
    "ROCE": 13.78
  },
  "COALINDIA.NS": {
    "ROE": 69.84,
    "name": "Coal India Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Energy",
    "ROCE": 52.95
  },
  "DRREDDY.NS": {
    "ROE": 4.84,
    "name": "Dr Reddy's Laboratories Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Consumer, Non-Cyclical",
    "ROCE": 5.32
  },
  "EICHERMOT.NS": {
    "ROE": 41.21,
    "name": "Eicher Motors Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Auto",
    "ROCE": 61.82
  },
  "GAIL.NS": {
    "ROE": 11.77,
    "name": "GAIL India Ltd",
    "sector": "NON-FINANCIAL",
    "ROCE": 16.88
  },
  "GRASIM.NS": {
    "ROE": 6.40,
    "name": "Grasim Industries Ltd",
    "sector": "NON-FINANCIAL",
    "ROCE": 11.63
  },
  "HCLTECH.NS": {
    "ROE": 27.50,
    "name": "HCL Technologies Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Technology",
    "ROCE": 31.02
  },
  "HDFC.NS": {
    "ROE": 18.44,
    "name": "H D F C",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 9.47
  },
  "HDFCBANK.NS": {
    "ROE": 17.87,
    "name": "HDFC Bank Ltd",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 7.32
  },
  "HEROMOTOCO.NS": {
    "ROE": 33.80,
    "name": "Hero MotoCorp Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Auto",
    "ROCE": 47.58
  },
  "HINDALCO.NS": {
    "ROE": 3.42,
    "sector": "NON-FINANCIAL",
    "name": "Hindalco Industries Ltd",
    "sub-sector": "Basic Materials",
    "ROCE": 6.11
  },
  "HINDUNILVR.NS": {
    "ROE": 77.21,
    "name": "Hindustan Unilever Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Consumer, Non-Cyclical",
    "ROCE": 90.96
  },
  "BRITANNIA.NS": {
    "ROE": 32.59,
    "name": "Britannia Industries Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Consumer, Non-Cyclical",
    "ROCE": 49.23
  },
  "ICICIBANK.NS": {
    "ROE": 6.81,
    "name": "ICICI Bank Ltd",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 5.24
  },
  "IBULHSGFIN.NS": {
    "ROE": 28.81,
    "name": "Indiabulls Housing Finance Ltd",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 11.21
  },
  "INDUSINDBK.NS": {
    "ROE": 16.48,
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "name": "IndusInd Bank Ltd",
    "ROCE": 7.97
  },
  "INFY.NS": {
    "ROE": 24.57,
    "name": "Infosys Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Technology",
    "ROCE": 30.21
  },
  "IOC.NS": {
    "ROE": 20.34,
    "name": "Indian Oil Corporation Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Energy",
    "ROCE": 21.79
  },
  "ITC.NS": {
    "ROE": 23.20,
    "name": "ITC Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Consumer, Non-Cyclical",
    "ROCE": 34.92
  },
  "JSWSTEEL.NS": {
    "ROE": 17.79,
    "name": "JSW Steel Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Basic Materials",
    "ROCE": 16.62
  },
  "KOTAKBANK.NS": {
    "ROE": 12.55,
    "name": "Kotak Mahindra Bank Ltd",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 7.93
  },
  "LT.NS": {
    "ROE": 11.32,
    "name": "Larse & Toubro Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Industrial",
    "ROCE": 14.95
  },
  "M&M.NS": {
    "ROE": 15.25,
    "name": "Mahindra & Mahindra Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Consumer, Cyclical",
    "ROCE": 18.97
  },
  "MARUTI.NS": {
    "ROE": 16.37,
    "name": "Maruti Suzuki India Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Auto",
    "ROCE": 23.17
  },
  "NTPC.NS": {
    "ROE": 10.45,
    "name": "NTPC Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Utilities",
    "ROCE": 7.48
  },
  "ONGC.NS": {
    "ROE": 10.53,
    "name": "Oil & Natural Gas Corp Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Energy",
    "ROCE": 15.03
  },
  "POWERGRID.NS": {
    "ROE": 15.81,
    "name": "Power Grid Corp of India Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Utilities",
    "ROCE": 13.60
  },
  "RELIANCE.NS": {
    "ROE": 11.15,
    "name": "Reliance Industries Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Energy",
    "ROCE": 12.11
  },
  "SBIN.NS": {
    "ROE": -2.34,
    "name": "State Bank of India",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 4.19
  },
  "SUNPHARMA.NS": {
    "ROE": 1.55,
    "name": "Sun Pharmaceutical Industries Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Consumer, Non-Cyclical",
    "ROCE": 2.47
  },
  "TCS.NS": {
    "ROE": 32.92,
    "name": "Tata Consultancy Services Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Technology",
    "ROCE": 41.19
  },
  "TATAMOTORS.NS": {
    "ROE": 0.00,
    "name": "Tata Motors Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Auto",
    "ROCE": 0.00
  },
  "TATASTEEL.NS": {
    "ROE": 11.76,
    "name": "Tata Steel Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Basic Materials",
    "ROCE": 14.38
  },
  "TECHM.NS": {
    "ROE": 21.96,
    "name": "Tech Mahindra Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Technology",
    "ROCE": 24.27
  },
  "TITAN.NS": {
    "ROE": 24.47,
    "name": "Titan Co Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Consumer, Non-Cyclical",
    "ROCE": 24.54
  },
  "ULTRACEMCO.NS": {
    "ROE": 8.95,
    "name": "UltraTech Cement Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Industrial",
    "ROCE": 12.10
  },
  "UPL.NS": {
    "ROE": 7.01,
    "name": "UPL Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Basic Materials",
    "ROCE": 7.91
  },
  "VEDL.NS": {
    "ROE": 3.18,
    "name": "Vedanta Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Basic Materials",
    "ROCE": 5.62
  },
  "WIPRO.NS": {
    "ROE": 17.36,
    "name": "Wipro Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Technology",
    "ROCE": 20.10
  },
  "YESBANK.NS": {
    "ROE": 17.67,
    "name": "Yes Bank Ltd",
    "sector": "FINANCIAL",
    "sub-sector": "Financial",
    "ROCE": 7.42
  },
  "ZEEL.NS": {
    "ROE": 37.61,
    "name": "Zee Entertainment Enterprises Ltd",
    "sector": "NON-FINANCIAL",
    "sub-sector": "Communications",
    "ROCE": 40.93
  }
}

