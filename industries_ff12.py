import pandas as pd
import numpy as np

# Fama-French 12 industry names (as per French's website)
FF12_NAMES = {
    1: 'NoDur',   # Consumer NonDurables
    2: 'Durbl',   # Consumer Durables
    3: 'Manuf',   # Manufacturing
    4: 'Enrgy',   # Oil, Gas, Coal
    5: 'Chems',   # Chemicals
    6: 'BusEq',   # Business Equipment
    7: 'Telcm',   # Telephone and Television Transmission
    8: 'Utils',   # Utilities
    9: 'Shops',   # Wholesale, Retail, Services
    10: 'Hlth',   # Healthcare, Medical
    11: 'Money',  # Finance
    12: 'Other',  # Other
}

def assign_ff12_industry(df, sic_col='sic', prefix='i', ind_code_col='FF_IND_CODE'):
    """
    Assign Fama-French 12-industry codes to a DataFrame using SIC codes.
    Adds:
        - integer industry code (1-12)
        - textual industry name
        - 12 one-hot columns (optional, default True)
    Params:
        df: pandas DataFrame with SIC codes
        sic_col: column name for SIC code (must be 4-digit integer or NaN)
        prefix: prefix for 12 binary columns ('i' → i1, i2, ...)
        ind_code_col: name for industry code column
    Returns:
        df: pandas DataFrame with new columns added
    """
    df = df.copy()

    def get_ff12_code(sic):
        if pd.isnull(sic):
            return np.nan
        sic = int(sic)
        # 1 NoDur: Consumer NonDurables
        if (100 <= sic <= 999) or (2000 <= sic <= 2399) or (2700 <= sic <= 2749) or (2770 <= sic <= 2799) or (3100 <= sic <= 3199) or (3940 <= sic <= 3989):
            return 1
        # 2 Durbl: Consumer Durables
        if (2500 <= sic <= 2519) or (2590 <= sic <= 2599) or (3630 <= sic <= 3659) or (3710 <= sic <= 3711) or (3714 == sic) or (3716 == sic) or (3750 <= sic <= 3751) or (3792 == sic) or (3900 <= sic <= 3939) or (3990 <= sic <= 3999):
            return 2
        # 3 Manuf: Manufacturing
        if (2520 <= sic <= 2589) or (2600 <= sic <= 2699) or (2750 <= sic <= 2769) or (3000 <= sic <= 3099) or (3200 <= sic <= 3569) or (3580 <= sic <= 3629) or (3700 <= sic <= 3709) or (3712 <= sic <= 3713) or (3715 == sic) or (3717 <= sic <= 3749) or (3752 <= sic <= 3791) or (3793 <= sic <= 3799) or (3830 <= sic <= 3839) or (3860 <= sic <= 3899):
            return 3
        # 4 Enrgy: Oil, Gas, and Coal Extraction and Products
        if (1200 <= sic <= 1399) or (2900 <= sic <= 2999):
            return 4
        # 5 Chems: Chemicals and Allied Products
        if (2800 <= sic <= 2829) or (2840 <= sic <= 2899):
            return 5
        # 6 BusEq: Business Equipment
        if (3570 <= sic <= 3579) or (3660 <= sic <= 3692) or (3694 <= sic <= 3699) or (3810 <= sic <= 3829) or (7370 <= sic <= 7379):
            return 6
        # 7 Telcm: Telephone and Television Transmission
        if (4800 <= sic <= 4899):
            return 7
        # 8 Utils: Utilities
        if (4900 <= sic <= 4949):
            return 8
        # 9 Shops: Wholesale, Retail, and Some Services
        if (5000 <= sic <= 5999) or (7200 <= sic <= 7299) or (7600 <= sic <= 7699):
            return 9
        # 10 Hlth: Healthcare
        if (2830 <= sic <= 2839) or (3693 == sic) or (3840 <= sic <= 3859) or (8000 <= sic <= 8099):
            return 10
        # 11 Money: Finance
        if (6000 <= sic <= 6999):
            return 11
        # 12 Other: All others
        return 12
        
    # Assign industry code
    df[ind_code_col] = df[sic_col].apply(get_ff12_code)
    # Assign textual name
    df['FF_IND'] = df[ind_code_col].map(FF12_NAMES)

    # Add 12 binary columns
    for i in range(1, 13):
        col = f'{prefix}{i}'
        df[col] = (df[ind_code_col] == i).astype(int)

    return df
