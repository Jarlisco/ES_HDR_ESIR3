import typer
from typing import List
from pathlib import Path
from colorama import Fore, Back
import visu_hdr

#===============================================
app = typer.Typer(help="Awesome CLI user manager.")

#===============================================
@app.command()
def CRF_HDR_TMO_LDR(fusion_type : str = typer.Argument("debevec", help="Choose between debevec or mentens fusion."),
                    pathprefix  : str = typer.Argument(..., help="Path prefix to images to merge. Path prefix is then completed with a number and the file extension ex: .img/img(1.jpg)"),
                    count       : int = typer.Argument(..., help="Number of images to merge. It will complete the path prefix starting from 1 to 'count' included."),
                    extension   : str = typer.Argument(..., help="Image file extension it will complete the path prefix")):
    
    
    """
    Uses images of diffrent exposure to create HDR image and then it is tone mapped to let you see the result.
    """

    if fusion_type == "debevec":
        visu_hdr.CRF_merge_Debevec(prefix,count,extension)
    elif fusion_type == "robertson":
        visu_hdr.CRF_merge_Robertson()
    else:
        typer.echo(Fore.RED + f"{fusion_type} is not supported for this command (try debevec or robertson)."+ Fore.RESET)

#===============================================
@app.command()
def LDR_FUSION_LDR(fusion_type: str = typer.Argument("debevec")):
    typer.echo(Fore.CYAN + "Uses multiple LDR images a better quality LDR." + Fore.RESET)

    if fusion_type == "mertens":
        visu_hdr.LDR_fusion_Mertens()
    else:
        typer.echo(Fore.RED + f"{fusion_type} is not supported for this command (try mertens)."+ Fore.RESET)

#===============================================
@app.command()
def HDR_TMO_LDR(name: str, fn : str, gamma: float):
    typer.echo(Fore.CYAN + "Opens HDR image and then tone map to display it." + Fore.RESET)

    if name == "mantiuk":
        visu_hdr.HDR_TMO_Mantiuk(fn, gamma)
    elif name == "reinhard":
        visu_hdr.HDR_TMO_Reinhard(fn, gamma)
    else:
        typer.echo(Fore.RED + f"{name} is not supported for this command (try mantiuk or reinhard)."+ Fore.RESET)

#===============================================
#===============================================
#===============================================
@app.command()
def HDR_TMO_norm(fn : str  = typer.Argument(..., help="Path to HDR image.")):
    
    """
    Tone map HDR images by norming aroung the maximum of luminance.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing tone mapping using normal operator." + Fore.RESET)
        visu_hdr.TMO_norm(fn._str)
    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)

#===============================================
@app.command()
def HDR_TMO_gamma(fn : str  = typer.Argument(..., help="Path to HDR image."),
                  gamma : float = typer.Argument(..., help="1/gamma is used as exponent.")):
    
    """
    Tone map HDR images using gamma operator.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing tone mapping using gamma operator." + Fore.RESET)
        visu_hdr.TMO_gamma(fn._str, gamma)
    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)
 
#===============================================
@app.command()
def HDR_TMO_exp(fn : str  = typer.Argument(..., help="Path to HDR image."),
                k : float = typer.Argument(..., help="Luminance multiplier."),
                q : float = typer.Argument(..., help="Average Luminance mitiplier.")):
    
    """
    Tone map HDR images using exponential operator.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing tone mapping using exponential operator." + Fore.RESET)
        visu_hdr.TMO_exp(fn._str, k, q)
    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)

#===============================================
@app.command()
def HDR_TMO_log(fn : Path = typer.Argument(..., help="Path to hdr image file."),
                k : float = typer.Argument(..., help="Luminance multiplier."),
                q : float = typer.Argument(..., help="Max Luminance multiplier.")):
    
    """
    Tone map HDR images using log operator.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing tone mapping using log operator." + Fore.RESET)
        visu_hdr.TMO_log(fn._str, k, q)
    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)

#===============================================
@app.command()
def HDR_TMO_local(fn    : Path  = typer.Argument(..., help="Path to hdr image file."),
                  alpha : float = typer.Argument(1., help="1-alpha is luminance denominator exponent")):
    
    """
    This a local based method to tone map HDR images.
    It uses local luminance normalization.
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing homemade local normal luminance tone mapping." + Fore.RESET)
        visu_hdr.TMO_local(fn._str, alpha)
    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)

#===============================================
@app.command()
def HDR_TMO_durand(fn : Path = typer.Argument(..., help="Path to hdr image file.")):

    """
    We tried to implement and homemade Durand tone mapping. 
    It uses bilateral filtering and base logarithme (log2).
    """

    if fn.is_file() and fn.suffix == ".hdr":
        typer.echo(Fore.CYAN + "Doing homemade Durand tone mapping." + Fore.RESET)
        visu_hdr.TMO_durand(fn._str)
    else:
        typer.echo(Fore.RED + "File doesn't exist or is not .hdr file." + Fore.RESET)


#===============================================
def main():
    app()

#===============================================
if __name__ == "__main__":
    main()
