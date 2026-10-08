"""MonteCarlopriceofaEuropean callagainsttheBlack-Scholesformula."""
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]/"src"))
import matplotlib #noqa:E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt #noqa:E402
import numpy as np #noqa:E402
from cfproject.european import bs_call,mc_call #noqa:E402
from cfproject.experiment import Experiment #noqa:E402

def main():
    ex=Experiment(__file__)
    cfg= ex.config
    S0,K,r,sigma,T=cfg["S0"],cfg["K"],cfg["r"],cfg["sigma"],cfg["T"]
    exact = bs_call(S0,K,r,sigma,T)
    rows=[]
    for i,n in enumerate(cfg["n_paths"]):
        price,se=mc_call(S0,K,r,sigma,T,n,ex.rng(offset=i))
        rows.append({"n_paths":n,"price":price,"se":se,"error":price-exact})
    print(f"Black-Scholesprice:{exact:.4f}")

    ex.save_table(rows,"prices",
                    fmt={"price":"{:.4f}","se":"{:.4f}","error":"{:+.4f}"})
    fig,ax =plt.subplots(figsize=(6,3.6))
    ax.errorbar([x["n_paths"] for x in rows],[x["price"] for x in rows],
                yerr=[2*x["se"] for x in rows],fmt="o-",capsize=3,
                label="MonteCarlo±2s.e.")
    ax.axhline(exact,color="gray",ls="--",label=f"Black-Scholes{exact:.4f}")
    ax.set_xscale("log")
    ax.set_xlabel("numberofpaths")
    ax.set_ylabel("callprice")
    ax.legend(frameon=False)
    ex.save_figure(fig)

if __name__ =="__main__":
    main()

