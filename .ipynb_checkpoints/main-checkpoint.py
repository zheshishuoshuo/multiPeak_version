from run_mcmc import run_mcmc
from likelihood import log_posterior
from interpolator import build_interp_list_for_lenses
from mock_generator import run_mock_simulation
import numpy as np
import multiprocessing


def main():
    mock_lens_data, mock_observed_data = run_mock_simulation(n_samples=100)
    logMh_grid = np.linspace(11.5, 14.0, 100)

    logMstar_list, detJ_list = build_interp_list_for_lenses(
        mock_observed_data, logMh_grid, zl=0.3, zs=2.0
    )

    # sampler = run_mcmc(
    #     data_df=mock_observed_data,
    #     logMstar_interp_list=logMstar_list,
    #     detJ_interp_list=detJ_list,
    #     use_interp=True,
    #     log_posterior_func=log_posterior,
    #     backend_file="mcmc_chain.h5",
    #     nwalkers=8,
    #     nsteps=1000,
    #     ndim=4,
    #     initial_guess=np.array([12.5, 0.3, 0.05, 0.05]),
    #     processes=4
    # )
    from likelihood import log_posterior, initializer_for_pool

    sampler = run_mcmc(
        data_df=mock_observed_data,
        logMstar_interp_list=logMstar_list,
        detJ_interp_list=detJ_list,
        use_interp=True,
        log_posterior_func=log_posterior,
        backend_file="mcmc_chain_no_cache.h5",
        nwalkers=16,
        nsteps=8000,
        ndim=4,
        initial_guess=np.array([12.7, 0.34, 0.1, 0.13]),
        processes=multiprocessing.cpu_count()
        )
    samples = sampler.get_chain(discard=1000, thin=10, flat=True)
    np.save("samples_final.npy", samples)



if __name__ == "__main__":
    main()
