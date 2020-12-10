import typer
from typing import List
from pathlib import Path
from colorama import Fore, Back
import numpy as np
import visu_hdr

#===============================================
app = typer.Typer()

#===============================================
# DEBUG :  Utilise toutes les commandes avec des
#          paramètres par défaut
#===============================================
@app.command()
def xGENERATE_ALL():

    """
    For debug purposes you can generate all images using default parameters.
    You need img1.jpg img2.jpg img3.jpg and 272_HDR2.hdr.
    """

    paths = [".\\img\\img1.jpg", ".\\img\\img2.jpg", ".\\img\\img3.jpg"]
    exposures = [1./80,1./25,1./200]
    fn = ".\\img\\272_HDR2.hdr"

    visu_hdr.CRF_merge_Debevec(   paths, exposures )
    visu_hdr.CRF_merge_Robertson( paths, exposures )
    visu_hdr.LDR_fusion_Mertens(  paths            )

    visu_hdr.HDR_TMO_Mantiuk(   str(fn), 1.3 )
    visu_hdr.HDR_TMO_Reinhard(  str(fn), 1.3 )

    visu_hdr.TMO_norm(   str(fn)        )
    visu_hdr.TMO_gamma(  str(fn), 2 )
    visu_hdr.TMO_exp(    str(fn), 1, 1  )
    visu_hdr.TMO_log(    str(fn), 1, 1  )
    visu_hdr.TMO_local(  str(fn), 1.5 )
    visu_hdr.TMO_durand( str(fn)        )


#==================================================
# RESULTAT 1 :  CRF à partir des expo -> HDR -> TMO
#==================================================
@app.command()
def CRF_to_HDR(fusion_type : str = typer.Argument("debevec", help="Choose between debevec or mertens fusion."),
               paths_and_exposures  : List[str] = typer.Argument(..., help="List of paths to images to merge along with list of exposure times of each images in the same order. Ex: im1.jpg im2.jpg 0.005 0.015")):

    
    """
    Uses images of diffrent exposure to create HDR image and then it is tone mapped to let you see the result.
    """

    paths = []
    exposures = []

    if fusion_type == "debevec" or fusion_type == "mertens" : 

        #==================================================================
        try:
            paths     = [Path(x) for x in paths_and_exposures[:len(paths_and_exposures)//2]]
            exposures = [float(x) for x in paths_and_exposures[len(paths_and_exposures)//2:]]
            pass
        except ValueError:
            typer.echo(Fore.RED + "You must specify the same number of paths and exposure times."+ Fore.RESET)
            return

        if (len(paths) == len(exposures)) and (len(exposures) > 0) and (len(paths) > 0): #We need same amount of files and exposure times
            
            for fn in paths: # Check is files exist
                if (not fn.is_file()): # if one don't return
                    typer.echo(Fore.RED + f"{fn} doesn't exist." + Fore.RESET)
                    return
        #==================================================================

            if fusion_type == "debevec":
                typer.echo(Fore.CYAN + "Using multiple exposure to create HDR image." + Fore.RESET)
                visu_hdr.CRF_merge_Debevec(paths,exposures)
                typer.echo(Fore.CYAN + "HDR created then Tone Mapped and saved as LDR_debevec.jpg." + Fore.RESET)

            elif fusion_type == "robertson":
                typer.echo(Fore.CYAN + "Using multiple exposure to create HDR image." + Fore.RESET)
                visu_hdr.CRF_merge_Robertson(paths,exposures)
                typer.echo(Fore.CYAN + "HDR created then Tone Mapped and saved as LDR_robertson.jpg." + Fore.RESET)

        else:
            typer.echo(Fore.RED + "You must specify the same number of paths and exposure times."+ Fore.RESET)
    
    else:
        typer.echo(Fore.RED + f"{fusion_type} is not supported for this command (try debevec or robertson)."+ Fore.RESET)


#==================================================
# RESULTAT 2 : Fusion directe des LDRs pour obtenir
#              une LDR haute qualité.
#==================================================
@app.command()
def LDR_to_HQLDR(fusion_type: str = typer.Argument("mertens", help="Choose your fusion algorithm (only mertens is available for now)."),
                 paths      : List[Path] = typer.Argument(..., help="List of paths to images to merge.")):
    """
    Fusion of mutiple LDR images to create an High Quality LDR image (HQLDR).
    """

    if len(paths) > 0:

        for fn in paths: # Check is files exist
            if (not fn.is_file()): # if one don't return
                typer.echo(Fore.RED + f"{fn} doesn't exist." + Fore.RESET)
                return

        if fusion_type == "mertens":
            typer.echo(Fore.CYAN + "Merge using Mertens' algorithm to create an HQLDR." + Fore.RESET)
            visu_hdr.LDR_fusion_Mertens(paths)
            typer.echo(Fore.CYAN + "HQLDR created and saved as fusion_mertens.jpg." + Fore.RESET)

        else:
            typer.echo(Fore.RED + f"{fusion_type} is not supported for this command (try mertens)."+ Fore.RESET)
    else:
        typer.echo(Fore.RED + "Error within paths list."+ Fore.RESET)

#=================================================
# RESULTAT 3 : TMO d'une image HDR avec la méthode
#              de Mantiuk ou Reinhard.
#=================================================
@app.command()
def HDR_to_LDR(tone_mapper: str = typer.Argument("mantiuk", help="Choose your tone mapper (mantiuk or reinhard)"), 
               path       : Path = typer.Argument(..., help="Path to HDR image."), 
               gamma      : float = typer.Argument(..., help="It is THE gamma.")):

    """
    Tone mapping HDR image to LDR using opencv implemented tone mappers.
    """

    if path.is_file() and path.suffix == ".hdr":
        if tone_mapper == "mantiuk":
            typer.echo(Fore.CYAN + "Doing tone mapping using Mantiuk tone mapper." + Fore.RESET)
            visu_hdr.HDR_TMO_Mantiuk(str(path), gamma)
            typer.echo(Fore.CYAN + "HDR Tone Mapped and saved as TMO_Mantiuk.jpg." + Fore.RESET)

        elif tone_mapper == "reinhard":
            typer.echo(Fore.CYAN + "Doing tone mapping using Reinhard tone mapper." + Fore.RESET)
            visu_hdr.HDR_TMO_Reinhard(str(path), gamma)
            typer.echo(Fore.CYAN + "HDR Tone Mapped and saved as TMO_Reinhard.jpg." + Fore.RESET)

        else:
            typer.echo(Fore.RED + f"{tone_mapper} is not supported for this command (try mantiuk or reinhard)."+ Fore.RESET)
    else:
        typer.echo(Fore.RED + f"{path} doesn't exist or is not .hdr file." + Fore.RESET)

#=====================================================
# RESULTAT 4 : Implémentation de différents opérateurs
#              de tone mapping.
#=====================================================
@app.command()
def HDR_TMO_norm(fn : Path  = typer.Argument(..., help="Path to HDR image.")):
    
    """
    ~ Tone map HDR images by norming aroung the maximum of luminance.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing tone mapping using normal operator." + Fore.RESET)
        visu_hdr.TMO_norm(str(fn))
        typer.echo(Fore.CYAN + "HDR Tone Mapped and saved as TMO_norm.jpg." + Fore.RESET)

    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)

#===============================================
@app.command()
def HDR_TMO_gamma(fn : Path  = typer.Argument(..., help="Path to HDR image."),
                  gamma : float = typer.Argument(..., help="1/gamma is used as exponent.")):
    
    """
    ~ Tone map HDR images using gamma operator.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing tone mapping using gamma operator." + Fore.RESET)
        visu_hdr.TMO_gamma(str(fn), gamma)
        typer.echo(Fore.CYAN + "HDR Tone Mapped and saved as TMO_gamma.jpg." + Fore.RESET)

    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)
 
#===============================================
@app.command()
def HDR_TMO_exp(fn : Path  = typer.Argument(..., help="Path to HDR image."),
                k : float = typer.Argument(1., help="Luminance multiplier."),
                q : float = typer.Argument(1., help="Average Luminance mitiplier.")):
    
    """
    ~ Tone map HDR images using exponential operator.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing tone mapping using exponential operator." + Fore.RESET)
        visu_hdr.TMO_exp(str(fn), k, q)
        typer.echo(Fore.CYAN + "HDR Tone Mapped and saved as TMO_exp.jpg." + Fore.RESET)

    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)

#===============================================
@app.command()
def HDR_TMO_log(fn : Path = typer.Argument(..., help="Path to hdr image file."),
                k : float = typer.Argument(1., help="Luminance multiplier."),
                q : float = typer.Argument(1., help="Max Luminance multiplier.")):
    
    """
    ~ Tone map HDR images using log operator.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing tone mapping using log operator." + Fore.RESET)
        visu_hdr.TMO_log(str(fn), k, q)
        typer.echo(Fore.CYAN + "HDR Tone Mapped and saved as TMO_log.jpg." + Fore.RESET)

    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)

#===============================================
@app.command()
def HDR_TMO_local(fn    : Path  = typer.Argument(..., help="Path to hdr image file."),
                  alpha : float = typer.Argument(1., help="1-alpha is luminance denominator exponent (for blurred luminance image)")):
    
    """
    ~ Tone map using a local based method.
    It uses local luminance normalization.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing homemade local normal luminance tone mapping." + Fore.RESET)
        visu_hdr.TMO_local(str(fn), alpha)
        typer.echo(Fore.CYAN + "HDR Tone Mapped and saved as TMO_local.jpg." + Fore.RESET)

    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)

#===============================================
# RESULTAT 6 : Implémentation à la main du tone
#              mapping de Durand.
#===============================================
@app.command()
def HDR_TMO_durand(fn : Path = typer.Argument(..., help="Path to hdr image file.")):

    """
    ~ Tone map using homemade Durand tone mapper. 
    It uses bilateral filtering and logarithme base 2 (log2).
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing homemade Durand tone mapping." + Fore.RESET)
        visu_hdr.TMO_durand(str(fn))
        typer.echo(Fore.CYAN + "HDR Tone Mapped and saved as TMO_durand.jpg." + Fore.RESET)

    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)


#===============================
# MAIN : Start typer application
#===============================
def main():
    app()

#===============================================
if __name__ == "__main__":
    main()
