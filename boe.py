comandos = {
    "Estado da Tela": {
        "Reading": {
            "Tela 1": {
                "Send Data": "ff 55 04 39 01 01 00 93",
                "ACK": "ff 55 06 39 01 01 00 00 00 3b",
                "Lenght": 10,
                "Header": "ff 55 06 39",
                "Display1": 5,
                "Display2": 6,
                "Estado": 7,
                "Zeros": "00 00",
                "CheckSum": "3B"
            },
            "Tela 2": {
                "Send Data": "ff 55 04 39 02 02 00 95",
                "ACK": "ff 55 06 39 01 01 00 00 00 3b",
                "Lenght": 10,
                "Header": "ff 55 06 39",
                "Display1": "02",
                "Display2": "02",
                "Estado": "00",
                "Zeros": "00 00",
                "CheckSum": "3B"
            },
            "Tela 1 e 2": {
                "Send Data": "ff 55 04 39 01 02 00 94",
                "ACK": "ff 55 06 39 01 01 00 00 00 3b",
                "Lenght": 10,
                "Header": "ff 55 06 39",
                "Display1": "01",
                "Display2": "02",
                "Estado": "00",
                "Zeros": "00 00",
                "CheckSum": "3B"
            },
        },
        "Setting": {
            "Desligar a Tela 1": {
                "Send Data": "FF 55 04 83 01 01 00 dd",
                "ACK": "ff 55 04 83 00 00 00 db"
            },
            "Desligar a Tela 2": {
                "Send Data": "ff 55 04 83 02 02 00 df",
                "ACK": "ff 55 04 83 00 00 00 db"
            },
            "Desligar a Tela 1 e 2": {
                "Send Data": "ff 55 04 83 01 02 00 de",
                "ACK": "ff 55 04 83 00 00 00 db"
            },
            "Ligar a Tela 1": {
                "Send Data": "FF 55 04 84 01 01 00 de",
                "ACK": "ff 55 04 84 00 00 00 dc"
            },
            "Ligar a Tela 2": {
                "Send Data": "ff 55 04 84 02 02 00 e0",
                "ACK": "ff 55 04 84 00 00 00 dc"
            },
            "Ligar a Tela 1 e 2": {
                "Send Data": "FF 55 04 84 01 02 00 df",
                "ACK": "ff 55 04 84 00 00 00 dc"
            }
        }
    },
    "Input Source": {
        "Reading": {
            "Tela 1": {
                "Send Data": "FF 55 04 42 01 01 00 9c",
                "ACK": "ff 55 04 42 01 01 02 9e"
            },
            "Tela 2": {
                "Send Data": "ff 55 04 42 02 02 00 9e",
                "ACK": "ff 55 04 42 02 02 03 a1"
            },
            "Tela 1 e 2": {
                "Send Data": "ff 55 04 42 01 02 00 9d",
                "ACK": "ff 55 04 42 01 01 02 9e"
            },
        },
        "Setting": {
            "Tela 1 HDMI 1": {
                "Send Data": "FF 55 04 82 01 01 02 de",
                "ACK": "ff 55 04 82 00 00 00 da"
            },
            "Tela 1 HDMI 2": {
                "Send Data": "FF 55 04 82 01 01 03 df",
                "ACK": "ff 55 04 82 00 00 00 da"
            },
            "Tela 1 DP": {
                "Send Data": "FF 55 04 82 01 01 01 dd",
                "ACK": "ff 55 04 82 00 00 00 da"
            },
            "Tela 2 HDMI 1": {
                "Send Data": "FF 55 04 82 02 02 02 e0",
                "ACK": "ff 55 04 82 00 00 00 da"
            },
            "Tela 2 HDMI 2": {
                "Send Data": "FF 55 04 82 02 02 03 e1",
                "ACK": "ff 55 04 82 00 00 00 da"
            },
            "Tela 2 DP": {
                "Send Data": "FF 55 04 82 02 02 01 df",
                "ACK": "ff 55 04 82 00 00 00 da"
            },
        }
    },
    "Input Signal Status": {
        "Reading": {
            "Tela 1": {
                "Send Data": "FF 55 04 57 01 01 00 b1",
                "ACK": "ff 55 04 57 01 01 00 b1"
            },
            "Tela 2": {
                "Send Data": "FF 55 04 57 02 02 00 b3",
                "ACK": "Sem resposta"
            },
            "Tela 1 e 2": {
                "Send Data": "FF 55 04 57 01 02 00 b2",
                "ACK": "ff 55 04 57 01 01 01 b2"
            },

            # "HDMI 2 OFF": {
            #     "Send Data": "FF 55 04 57 02 02 00 b3",
            #     "ACK": "Sem resposta"
            # },
            # "HDMI 1 / 2 OFF": {
            #     "Send Data": "FF 55 04 57 01 02 00 b2",
            #     "ACK": "ff 55 04 57 01 01 01 b2"
            # }
        }
    },
    "Brightness": {
        "Reading": {
            "Tela 1": {
                "Send Data": "FF 55 04 40 01 01 00 9a",
                "ACK": "FF 55 04 40 01 01 32 cc"
            },
            "Tela 2": {
                "Send Data": "FF 55 04 40 02 02 00 9a",
                "ACK": "FF 55 04 40 01 01 33 cd"
            },
            "Tela 1 e 2": {
                "Send Data": "FF 55 04 40 01 02 00 9b",
                "ACK": "FF 55 04 40 01 01 33 cd"
            },
        },
        "Setting": {
            "Tela 2": {
                "Send Data": "FF 55 04 30 02 02 32 be",
                "ACK": "ff 55 04 30 00 00 00 88"
            },
            "Tela 1 / 2": {
                "Send Data": "FF 55 04 30 01 02 32 bd",
                "ACK": "ff 55 04 30 00 00 00 88"
            },
            "Tela 1": {
                "Send Data": "FF 55 04 30 01 01 32 bc",
                "ACK": "ff 55 04 30 00 00 00 88"
            }
        }
    },
    "Backlight": {
        "Reading": {
            "Tela 1": {
                "Send Data": "FF 55 04 56 01 01 00 b0",
                "ACK": "ff 55 04 56 01 01 0a ba"
            },
            "Tela 2": {
                "Send Data": "ff 55 04 56 02 02 00 b2",
                "ACK": "FF 55 04 56 02 02 64 14"
            },
            "Tela 1 e 2": {
                "Send Data": "ff 55 04 56 01 02 0a bb",
                "ACK": "ff 55 04 56 01 01 64 14"
            },
        },
        "Setting": {
            "Tela 1": {
                "Send Data": "FF 55 04 66 01 01 64 24",
                "ACK": "ff 55 04 66 00 00 00 be"
            },
            "Tela 2": {
                "Send Data": "FF 55 04 66 02 02 64 26",
                "ACK": "ff 55 04 66 00 00 00 be"
            },
            "Tela 1 e 2": {
                "Send Data": "FF 55 04 66 02 02 64 25",
                "ACK": "ff 55 04 66 00 00 00 be"
            },
        }
    },
    'Relay': {
        'Setting': {
            'Relay - 0 OFF': {
                'Send Data': 'ff 55 04 ad 00 00 00 05',
                'ACK': 'ACK for Relay - 0 OFF'
            },
            'Relay - 1 OFF': {
                'Send Data': 'ff 55 04 ad 01 00 00 06',
                'ACK': 'ACK for Relay - 1 OFF'
            },
            'Relay - 2 OFF': {
                'Send Data': 'ff 55 04 ad 02 00 00 07',
                'ACK': 'ACK for Relay - 2 OFF'
            },
            'Relay - 3 OFF': {
                'Send Data': 'ff 55 04 ad 03 00 00 08',
                'ACK': 'ACK for Relay - 3 OFF'
            },
            'Relay - 4 OFF': {
                'Send Data': 'ff 55 04 ad 04 00 00 09',
                'ACK': 'ACK for Relay - 4 OFF'
            },
            'Relay - 5 OFF': {
                'Send Data': 'ff 55 04 ad 05 00 00 0a',
                'ACK': 'ACK for Relay - 5 OFF'
            },
            'Relay - 0 ON': {
                'Send Data': 'ff 55 04 ad 00 01 00 06',
                'ACK': 'ACK for Relay - 0 ON'
            },
            'Relay - 1 ON': {
                'Send Data': 'ff 55 04 ad 01 01 00 07',
                'ACK': 'ACK for Relay - 1 ON'
            },
            'Relay - 2 ON': {
                'Send Data': 'ff 55 04 ad 02 01 00 08',
                'ACK': 'ACK for Relay - 2 ON'
            },
            'Relay - 3 ON': {
                'Send Data': 'ff 55 04 ad 03 01 00 09',
                'ACK': 'ACK for Relay - 3 ON'
            },
            'Relay - 4 ON': {
                'Send Data': 'ff 55 04 ad 04 01 00 0a',
                'ACK': 'ACK for Relay - 4 ON'
            },
            'Relay - 5 ON': {
                'Send Data': 'ff 55 04 ad 05 01 00 0b',
                'ACK': 'ACK for Relay - 5 ON'
            }
        }
    },
}

brilho = {
    # 1: {
    "Tela 1": {
        10: {
            "Send Data": "ff 55 04 66 01 01 0a ca",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        20: {
            "Send Data": "ff 55 04 66 01 01 14 d4",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        30: {
            "Send Data": "ff 55 04 66 01 01 1e de",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        40: {
            "Send Data": "ff 55 04 66 01 01 28 e8",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        50: {
            "Send Data": "ff 55 04 66 01 01 32 f2",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        60: {
            "Send Data": "ff 55 04 66 01 01 3c fc",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        70: {
            "Send Data": "ff 55 04 66 01 01 46 06",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        80: {
            "Send Data": "ff 55 04 66 01 01 50 10",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        90: {
            "Send Data": "ff 55 04 66 01 01 5a 1a",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        100: {
            "Send Data": "ff 55 04 66 01 01 64 24",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
    },
    # 2: {
    "Tela 2": {
        10: {
            "Send Data": "ff 55 04 66 02 02 0a cc",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        20: {
            "Send Data": "ff 55 04 66 02 02 14 d6",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        30: {
            "Send Data": "ff 55 04 66 02 02 1e e0",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        40: {
            "Send Data": "ff 55 04 66 02 02 28 ea",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        50: {
            "Send Data": "ff 55 04 66 02 02 32 f4",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        60: {
            "Send Data": "ff 55 04 66 02 02 3c fe",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        70: {
            "Send Data": "ff 55 04 66 02 02 46 08",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        80: {
            "Send Data": "ff 55 04 66 02 02 50 12",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        90: {
            "Send Data": "ff 55 04 66 02 02 5a 1c",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        100: {
            "Send Data": "ff 55 04 66 02 02 64 26",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
    },
    # 0: {
    "Telas 1 e 2": {
        10: {
            "Send Data": "ff 55 04 66 01 02 0a cb",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        20: {
            "Send Data": "ff 55 04 66 01 02 14 d5",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        30: {
            "Send Data": "ff 55 04 66 01 02 1e df",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        40: {
            "Send Data": "ff 55 04 66 01 02 28 e9",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        50: {
            "Send Data": "ff 55 04 66 01 02 32 f3",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        60: {
            "Send Data": "ff 55 04 66 01 02 3c fd",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        70: {
            "Send Data": "ff 55 04 66 01 02 46 07",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        80: {
            "Send Data": "ff 55 04 66 01 02 50 11",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        90: {
            "Send Data": "ff 55 04 66 01 02 5a 1b",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
        100: {
            "Send Data": "ff 55 04 66 01 02 64 25",
            "ACK": "ff 55 04 66 00 00 00 be"
        },
    },
}