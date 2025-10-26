"""
********************************************************************************
Author:     SITRAKA FORLER (lux-aiops.com)
            Python translation based on original SAS code by:
            Ed deHaan (staff.washington.edu/edehaan)
            Xue Li checked for updates on 3/24/2021

Purpose:    To assign Fama-French 5 industry codes based on 4-digit SIC codes

Version:    1.0 - Python translation - 10/26/2025

Notes:      5 Industry classification codes obtained from French's website
            http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
            
            Original SAS macro versions:
            1.0 - 2/17/11
            3/24/21 - rechecked assignments based on current classifications
                      No changes made
********************************************************************************
"""

import pandas as pd
import numpy as np

# Fama-French 5 industry names (as per French's website)
FF5_NAMES = {
    1: 'Cnsmr',  # Consumer Durables, NonDurables, Wholesale, Retail, and Some Services
    2: 'Manuf',  # Manufacturing, Energy, and Utilities
    3: 'HiTec',  # Business Equipment, Telephone and Television Transmission
    4: 'Hlth',   # Healthcare, Medical Equipment, and Drugs
    5: 'Other',  # Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment, Finance
}

def assign_ff5_industry(df, sic_col='sic', prefix='i', ind_code_col='FF_IND_CODE'):
    """
    Assign Fama-French 5-industry codes to a DataFrame using SIC codes.
    
    Adds to the DataFrame:
        - ind_code_col: integer industry code (1-5)
        - 'FF_IND': textual industry name
        - 5 one-hot encoded columns (prefix1, prefix2, ..., prefix5)
    
    Parameters:
        df: pandas DataFrame with SIC codes
        sic_col: column name for SIC code (must be 4-digit integer or NaN)
        prefix: prefix for 5 binary columns ('i' → i1, i2, ..., i5)
        ind_code_col: name for industry code column
    
    Returns:
        df: pandas DataFrame with new columns added
    """
    df = df.copy()

    def get_ff5_code(sic):
        if pd.isnull(sic):
            return np.nan
        sic = int(sic)
        
        # 1 Cnsmr: Consumer Durables, NonDurables, Wholesale, Retail, and Some Services
        if (100 <= sic <= 999) or (2000 <= sic <= 2399) or (2700 <= sic <= 2749) or \
           (2770 <= sic <= 2799) or (3100 <= sic <= 3199) or (3940 <= sic <= 3989) or \
           (2500 <= sic <= 2519) or (2590 <= sic <= 2599) or (3630 <= sic <= 3659) or \
           (3710 <= sic <= 3711) or (3714 == sic) or (3716 == sic) or \
           (3750 <= sic <= 3751) or (3792 == sic) or (3900 <= sic <= 3939) or \
           (3990 <= sic <= 3999) or (5000 <= sic <= 5999) or (7200 <= sic <= 7299) or \
           (7600 <= sic <= 7699):
            return 1
        
        # 2 Manuf: Manufacturing, Energy, and Utilities
        if (2520 <= sic <= 2589) or (2600 <= sic <= 2699) or (2750 <= sic <= 2769) or \
           (2800 <= sic <= 2829) or (2840 <= sic <= 2899) or (3000 <= sic <= 3099) or \
           (3200 <= sic <= 3569) or (3580 <= sic <= 3629) or (3700 <= sic <= 3709) or \
           (3712 <= sic <= 3713) or (3715 == sic) or (3717 <= sic <= 3749) or \
           (3752 <= sic <= 3791) or (3793 <= sic <= 3799) or (3830 <= sic <= 3839) or \
           (3860 <= sic <= 3899) or (1200 <= sic <= 1399) or (2900 <= sic <= 2999) or \
           (4900 <= sic <= 4949):
            return 2
        
        # 3 HiTec: Business Equipment, Telephone and Television Transmission
        if (3570 <= sic <= 3579) or (3622 == sic) or (3660 <= sic <= 3692) or \
           (3694 <= sic <= 3699) or (3810 <= sic <= 3839) or (7370 <= sic <= 7372) or \
           (7373 == sic) or (7374 == sic) or (7375 == sic) or (7376 == sic) or \
           (7377 == sic) or (7378 == sic) or (7379 == sic) or (7391 == sic) or \
           (8730 <= sic <= 8734) or (4800 <= sic <= 4899):
            return 3
        
        # 4 Hlth: Healthcare, Medical Equipment, and Drugs
        if (2830 <= sic <= 2839) or (3693 == sic) or (3840 <= sic <= 3859) or \
           (8000 <= sic <= 8099):
            return 4
        
        # 5 Other: Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment, Finance
        return 5
        
    # Assign industry code
    df[ind_code_col] = df[sic_col].apply(get_ff5_code)
    
    # Assign textual name
    df['FF_IND'] = df[ind_code_col].map(FF5_NAMES)

    # Add 5 binary columns (one-hot encoding)
    for i in range(1, 6):
        col = f'{prefix}{i}'
        df[col] = (df[ind_code_col] == i).astype(int)

    return df


# Example Usage:
if __name__ == "__main__":
    # Example DataFrame with various SIC codes
    df = pd.DataFrame({
        'sic': [1311, 2834, 3571, 7372, 3991, 5001, 6021, 8001, 100, 1500, None]
    })

    # Assign Fama-French codes
    df_ff5 = assign_ff5_industry(df, sic_col='sic', prefix='i', ind_code_col='FF_IND_CODE')

    print(df_ff5)
    
    # To get list of all industry dummy columns (equivalent to global macro variable)
    industry_fe_columns = [f'i{i}' for i in range(1, 6)]
    print(f"\nIndustry FE columns: {' '.join(industry_fe_columns)}")
