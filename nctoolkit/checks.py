import xarray as xr
from nctoolkit.runthis import run_this
from nctoolkit.utils import is_curvilinear
import subprocess


def check(self):
    """
    Check contents of files for common data problems.
    """

    print("*****************************************")
    print("Checking data types")
    print("*****************************************")
    self_contents = self.contents
    list1 = self_contents.reset_index(drop=True).data_type
    positions = [ind for ind, x in enumerate(list1) if x.startswith("I")]
    if len(positions):
        bad = list(self_contents.reset_index(drop=True).data_type[positions])

    if len(positions) > 0:
        check = ",".join(bad)
        if "," in check:
            print(
                f"The variable(s) {check} have integer data type. Consider setting data type to float 'F64' or 'F32' using set_precision."
            )
        else:
            print(
                f"The variable {check} has integer data type. Consider setting data type to float 'F64' or 'F32' using set_precision."
            )
    else:
        print("Variable checks passed")

    print("*****************************************")
    print("Running CF-compliance checks")
    print("*****************************************")

    cf_checker = True
    try:
        import cfchecker
    except:
        cf_checker = False
        print(
            "cfchecker is not available. Run 'pip install cfchecker' to check files for CF-compliance!"
        )

    if cf_checker:
        for ff in self:
            ds = xr.open_dataset(ff, decode_times=False)
            if "Conventions" not in list(ds.attrs.keys()):
                print(f"No CF-conventions in {ff}")
            else:
                version = ds.attrs["Conventions"].split("-")[1]

                command = f"cfchecks -v {version} {ff}"
                out = subprocess.Popen(
                    command,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                result, ignore = out.communicate()

                result_split = result.decode("utf-8").split("\n")
                splits = [
                    index
                    for index, value in enumerate(result_split)
                    if "Checking variable" in value
                ]
                end = [
                    index
                    for index, value in enumerate(result_split)
                    if "ERRORS dete" in value
                ][0]
                for i in range(0, len(splits)):
                    if i < (len(splits) - 1):

                        i_result = result_split[splits[i] : splits[i + 1]]
                        i_result = "\n".join(i_result)
                        if "ERROR: " in i_result:
                            i_result = i_result.replace(
                                "Checking variable:", "Issue with variable:"
                            )
                            print(i_result)
                    else:
                        i_result = result_split[splits[i] : end]
                        i_result = "\n".join(i_result)
                        if "ERROR: " in i_result:
                            i_result = i_result.replace(
                                "Checking variable:", "Issue with variable:"
                            )
                            print(i_result)

    print("*****************************************")
    print("Checking grid consistency")
    print("*****************************************")

    for ff in self:
        command = f"cdo griddes {ff}"
        out = subprocess.Popen(
                    command,
                    shell=True,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
        result, ignore = out.communicate()

        result = result.decode("utf-8")
        if result.count("gridID") > 1:
            print("Dataset file(s) contain variables with different grids.")






