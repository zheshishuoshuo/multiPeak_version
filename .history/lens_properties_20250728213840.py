from lens_solver import solve_single_lens
from lens_model import kpc_to_arcsec, LensModel
from sl_cosmology import Dang
import numpy as np


def lens_properties(model, beta_unit=0.5, logalpha_sps=0.1):
   xA, xB = solve_single_lens(model, beta_unit)
   kappaA = model.kappa(xA)
   kappaB = model.kappa(xB)
   gammaA = model.gamma(xA)
   gammaB = model.gamma(xB)
   magnificationA = model.mu_from_rt(xA)
   magnificationB = model.mu_from_rt(xB)
   kappa_starA = model.kappa_star(xA)
   kappa_starB = model.kappa_star(xB)
   alphaA = model.alpha(xA)
   alphaB = model.alpha(xB)  
       
   sA = 1- kappa_starA/kappaA
   sB = 1- kappa_starB/kappaB  

   logMsps = model.logM_star - logalpha_sps
   scatter_Mstar = 0.1  # [Msun] 源质量的散射
   logMsps_observed = logMsps + np.random.normal(loc=0.0, scale=scatter_Mstar)  # 添加噪声

   einstein_radius = model.einstein_radius()  # [kpc]
   einstein_radius_arcsec = kpc_to_arcsec(einstein_radius, model.zl, Dang)  # [arcsec]

   return {
       'xA': xA, 'xB': xB, 'beta': beta_unit,
       'kappaA': kappaA, 'kappaB': kappaB,
       'gammaA': gammaA, 'gammaB': gammaB,
       'magnificationA': magnificationA, 'magnificationB': magnificationB,
       'kappa_starA': kappa_starA, 'kappa_starB': kappa_starB,
       'alphaA': alphaA, 'alphaB': alphaB,
       'sA': sA, 'sB': sB,
       'logMsps_observed': logMsps_observed,  # [Msun]
       'logMsps': logMsps,  # [Msun]
       'einstein_radius_kpc': einstein_radius,
       'einstein_radius_arcsec': einstein_radius_arcsec
   }

   
   
# add source properties

def observed_data(input_df, caustic= False):
   """
   计算 lens 的属性，并返回包含源属性的字典
   """
   mag_source = input_df['mag_source'].values[0]  # [mag]
   maximum_magnitude = input_df['maximum_magnitude'].values[0]  # [mag]
   beta_unit = input_df['beta_unit'].values[0]  # [kpc]
   logalpha_sps = input_df['logalpha_sps'].values[0]
   logM_star = input_df['logM_star'].values[0]  # [Msun]
   logM_halo = input_df['logM_halo'].values[0]  # [Msun]
   logRe = input_df['logRe'].values[0]  # [kpc]
   zl = input_df['zl'].values[0]  # [redshift]
   zs = input_df['zs'].values[0]  # [redshift]

   model = LensModel(logM_star=logM_star, logM_halo=logM_halo, logRe=logRe, zl=zl, zs=zs)
   properties = lens_properties(model, beta_unit, logalpha_sps)

   # magnificationA, magnificationB = properties['magnificationA'], properties['magnificationB']
   
   scatter_mag = 0.1  # [mag] 源光度的散射
   properties['scatter_mag'] = scatter_mag
   magnitude_observedA = mag_source - 2.5 * np.log10(properties['magnificationA']) + np.random.normal(loc=0.0, scale=scatter_mag)
   magnitude_observedB = mag_source - 2.5 * np.log10(properties['magnificationB']) + np.random.normal(loc=0.0, scale=scatter_mag)

   # no observed error
   if magnitude_observedA > maximum_magnitude or magnitude_observedB > maximum_magnitude:
       properties['is_lensed'] = False
   else:
       properties['is_lensed'] = True

   # 添加源属性
   properties['magnitude_observedA'] = magnitude_observedA  # [mag]
   properties['magnitude_observedB'] = magnitude_observedB  # [mag]
   properties['mag_source'] = mag_source  # [mag]
   properties['maximum_magnitude'] = maximum_magnitude  # [mag]
   properties['beta_unit'] = beta_unit  # [kpc]
   properties['logalpha_sps'] = logalpha_sps  # [Msun]
   properties['logM_star'] = model.logM_star
   properties['logM_halo'] = model.logM_halo
   properties['logRe'] = model.logRe
   properties['zl'] = model.zl
   properties['zs'] = model.zs

   if caustic:
       properties['ycaustic_kpc'] = model.solve_ycaustic()
       properties['ycaustic_arcsec'] = model.solve_ycaustic_arcsec()
       properties['xradcrit_kpc'] = model.solve_xradcrit()
       properties['xradcrit_arcsec'] = kpc_to_arcsec(properties['xradcrit_kpc'], model.zl, Dang)
   
   return properties


