# from numba import jit
from math import fabs
import json
import time
import pandas as pd

# define the spreadsheet that we will get data from later
spreadsheet = pd.read_excel('C:/Users/m337l400/Documents/GitHub/py_glacier_flowmodel/Specs_03473.xlsx')

# constants
dt = 1 / 5000000   # chosen to make it run a bit faster than one day at a time (originally: 1/200) 5000000
iterations = 1000000000  # number of iterations to run 

# # dx = 500.0  ### LETS DERIVE THIS INSTEAD OF DECLARING IT
# L = 100.0  # Model length in kilometers
# gridpoints = 200  # Number of gridpoints we want to calculate
# dx = L / gridpoints * 1000  # distance between gridpoints in meters

# Lets make this to glacier 15.03473 specs
L = 23.939  # Model length in kilometers
gridpoints = 90 # len(spreadsheet["Bed_elevation"]) #comes out to 501  # Number of gridpoints we want to calculate (497 makes it about 50m, 90 makes it 266m spacing) 
dx = (L / gridpoints) * 1000  # distance between gridpoints in meters

# Flow law stuff
A = 3e-16  # could be as small as -24, Pa/
rho = 917  # density of ice, KG/M^3 (need kg since our A is Pa, which has Newtons, which is kg)
g = 9.81  # gravity
n = 3.0
Afl = ((2 * A) / (n + 2)) * (rho * g) ** n
print(A, Afl)

# create a list to hold our ice elevation of a length based on the number of gridpoints
# ice_elevation = [0] * gridpoints  # this line is for starting at zero
# ice_elevation = [7806.285,7744.805,7707.702,7679.354,7642.893,7584.225,7524.137,7468.187,7418.735,7356.889,7300.951,7264.080,7240.266,7217.350,7187.459,7147.501,7131.854,7120.446,7095.410,7070.423,7045.093,7012.166,6986.525,6968.729,6959.647,6952.075,6947.601,6943.162,6934.249,6927.275,6918.187,6911.743,6901.712,6894.188,6887.444,6880.458,6872.961,6852.962,6831.380,6809.847,6790.696,6781.847,6773.464,6770.793,6766.926,6762.733,6758.878,6754.515,6749.578,6740.922,6733.849,6718.013,6700.168,6681.134,6664.095,6655.867,6649.598,6641.167,6633.392,6625.521,6616.937,6607.818,6599.411,6590.124,6581.416,6574.431,6568.688,6563.472,6558.037,6549.857,6541.927,6540.217,6535.932,6508.968,6423.718,6402.292,6388.621,6371.696,6358.266,6343.264,6325.818,6316.414,6310.838,6308.255,6308.137,6307.408,6304.532,6303.118,6301.306,6298.144,6292.751,6287.862,6278.274,6271.318,6265.378,6261.253,6256.360,6254.238,6250.118,6245.593,6239.326,6234.368,6223.490,6214.877,6202.346,6194.792,6180.352,6168.674,6171.025,6169.980,6169.731,6161.919,6141.809,6127.011,6098.375,6070.756,6014.069,5961.937,5932.231,5925.105,5931.688,5943.484,5936.625,5917.794,5887.818,5854.444,5818.443,5806.808,5795.529,5790.985,5784.965,5781.298,5777.429,5777.529,5775.317,5772.161,5772.776,5769.360,5766.792,5762.562,5756.078,5754.176,5749.461,5742.063,5736.267,5727.109,5721.432,5719.651,5721.198,5722.062,5728.213,5725.005,5717.722,5708.072,5705.083,5710.728,5691.617,5679.883,5659.519,5631.730,5584.488,5535.531,5494.173,5480.593,5475.935,5475.663,5477.320,5479.596,5477.926,5478.196,5476.365,5475.181,5479.869,5482.851,5484.083,5487.700,5484.949,5487.246,5483.092,5473.239,5466.406,5454.411,5423.594,5408.050,5372.527,5249.342,5243.235,5240.689,5231.004,5217.913,5201.827,5183.498,5166.731,5153.639,5142.485,5130.064,5119.777,5112.602,5106.890,5102.446,5099.092,5094.428,5090.016,5086.063,5082.118,5076.994,5071.555,5066.058,5061.855,5057.027,5054.163,5050.266,5042.580,5035.881,5030.737,5026.024,5023.188,5020.839,5017.597,5016.853,5019.241,5016.857,5015.811,5003.687,5001.725,5004.706,5004.390,5010.786,5012.779,5016.726,5011.594,5006.354,5005.070,5005.474,5003.594,5003.569,5002.835,5002.585,5001.010,4994.033,4978.170,4970.205,4969.572,4967.815,4964.607,4961.288,4964.899,4965.518,4962.949,4961.130,4960.062,4959.369,4959.148,4960.654,4965.676,4958.539,4955.754,4954.709,4946.763,4944.971,4939.476,4932.555,4934.418,4936.777,4931.894,4942.246,4944.376,4947.772,4937.661,4942.577,4953.627,4961.049,4957.059,4948.615,4949.366,4947.519,4951.848,4951.633,4949.212,4944.730,4946.749,4951.622,4953.957,4955.109,4951.424,4953.424,4950.443,4939.894,4932.074,4930.702,4931.707,4944.542,4942.626,4940.328,4929.756,4922.668,4919.838,4906.871,4909.494,4914.328,4912.629,4907.826,4905.013,4904.864,4895.955,4900.856,4902.701,4898.782,4895.624,4894.199,4884.787,4888.701,4916.487,4935.092,4921.066,4910.012,4895.196,4883.710,4883.271,4882.972,4885.994,4891.394,4897.351,4891.961,4896.243,4890.573,4885.030,4883.548,4885.295,4892.950,4890.667,4879.941,4872.302,4861.797,4862.871,4849.760,4842.255,4835.270,4843.728,4840.170,4850.115,4844.703,4841.137,4838.904,4837.477,4836.211,4839.730,4837.861,4843.202,4849.548,4842.786,4838.873,4853.401,4847.908,4828.900,4822.408,4820.994,4805.008,4806.153,4810.531,4806.038,4804.566,4812.900,4813.747,4815.615,4813.657,4810.440,4805.394,4804.604,4800.625,4818.138,4813.016,4800.972,4800.583,4808.403,4805.018,4792.724,4786.040,4793.169,4788.963,4792.556,4784.511,4788.765,4786.722,4784.648,4782.739,4768.530,4765.833,4764.839,4778.069,4771.887,4751.381,4758.479,4754.505,4749.124,4759.261,4764.044,4767.367,4761.038,4756.822,4743.042,4742.442,4756.458,4750.118,4750.801,4734.918,4732.845,4738.327,4743.808,4731.963,4726.542,4729.101,4742.088,4753.445,4743.079,4741.189,4741.989,4748.270,4760.060,4770.624,4757.842,4750.356,4730.732,4735.296,4730.147,4734.424,4749.734,4748.351,4742.064,4751.336,4748.541,4733.340,4719.523,4713.796,4731.469,4726.843,4708.705,4703.863,4698.082,4700.094,4703.924,4704.877,4714.465,4696.395,4695.993,4706.692,4722.424,4707.098,4705.141,4707.176,4695.672,4691.786,4691.561,4694.925,4696.788,4708.075,4711.498,4713.042,4719.487,4698.211,4696.440,4688.285,4687.588,4693.352,4702.091,4708.775,4710.579,4690.711,4686.264,4695.261,4700.950,4693.787,4701.734,4695.147,4674.263,4670.145,4669.876,4669.757,4669.588,4669.990,4673.196,4674.792,4672.511,4691.434,4683.371,4672.170,4672.852,4682.468,4685.198,4684.415,4668.882,4668.852,4669.655,4669.798,4668.813,4668.965,4668.490]
ice_elevation = spreadsheet['Koshi_DEM'].tolist()

# create a list of bed elevations the same size of our ice_elevation list, set to 0 for now
# bed_elevation = [0] * gridpoints  # this line is for starting at zero
# bed_elevation = [7799.151,7738.190,7701.087,7664.205,7614.517,7549.831,7487.419,7433.363,7384.669,7316.302,7256.151,7218.256,7185.174,7162.258,7128.333,7086.115,7076.787,7065.379,7043.153,7016.704,6989.732,6955.948,6924.694,6901.324,6892.243,6878.596,6868.198,6863.759,6838.029,6832.387,6819.768,6806.628,6777.039,6760.521,6753.777,6744.564,6735.972,6715.973,6697.747,6677.773,6663.034,6661.744,6653.477,6647.622,6638.599,6628.543,6629.914,6616.587,6614.262,6605.606,6601.945,6590.142,6572.298,6558.646,6537.631,6540.492,6533.038,6512.346,6499.400,6491.529,6479.550,6468.644,6460.237,6449.745,6440.732,6431.654,6426.636,6422.778,6419.299,6413.327,6407.267,6405.557,6403.718,6378.192,6297.173,6275.748,6264.536,6239.794,6226.425,6204.327,6178.824,6167.044,6148.829,6143.231,6133.672,6129.323,6121.300,6112.527,6110.714,6101.575,6092.304,6087.415,6074.899,6070.633,6061.939,6059.280,6066.605,6061.283,6079.871,6081.617,6080.292,6075.334,6068.546,6063.710,6055.784,6053.603,6044.055,6021.206,6023.557,6017.943,6014.688,6006.876,5990.538,5978.130,5948.571,5921.563,5864.785,5813.649,5783.672,5774.111,5776.225,5788.022,5775.800,5746.694,5713.449,5678.275,5646.111,5636.268,5619.456,5609.119,5595.335,5583.054,5559.883,5551.479,5538.172,5525.908,5508.472,5502.673,5491.678,5482.566,5476.083,5477.536,5480.356,5472.958,5476.822,5480.215,5474.538,5487.529,5495.033,5503.175,5522.673,5519.465,5517.372,5514.612,5525.788,5533.526,5522.292,5517.302,5499.482,5473.223,5426.754,5378.793,5337.386,5319.549,5308.128,5299.432,5283.147,5285.423,5274.982,5267.819,5262.619,5263.244,5272.810,5280.809,5288.253,5300.258,5306.933,5327.421,5323.268,5322.271,5323.653,5321.786,5306.380,5326.174,5316.851,5196.803,5170.328,5169.113,5110.588,5094.730,5074.035,5055.258,5032.270,5020.006,5001.546,4980.199,4968.861,4953.225,4947.513,4936.035,4925.690,4913.002,4901.014,4889.157,4876.138,4861.012,4855.573,4832.268,4819.304,4806.951,4796.881,4784.226,4769.458,4757.616,4750.097,4742.101,4734.582,4732.234,4725.088,4724.142,4727.616,4724.229,4719.789,4702.742,4698.279,4702.952,4704.364,4714.392,4716.385,4742.418,4736.956,4731.715,4728.322,4728.910,4725.517,4725.778,4734.564,4736.675,4755.572,4758.661,4748.788,4734.666,4732.931,4734.106,4730.897,4731.150,4733.161,4720.477,4731.354,4735.848,4731.646,4731.847,4737.308,4745.247,4756.525,4755.239,4753.500,4752.794,4744.654,4742.863,4735.888,4731.488,4752.371,4743.355,4730.358,4707.162,4708.872,4734.544,4716.534,4679.524,4657.584,4648.398,4628.300,4603.761,4604.512,4587.197,4582.765,4579.913,4577.492,4576.299,4583.840,4588.713,4597.062,4599.882,4598.219,4600.219,4602.971,4593.186,4585.366,4584.836,4586.328,4602.229,4607.103,4615.162,4604.590,4616.463,4624.194,4611.227,4616.461,4617.677,4613.283,4622.629,4632.132,4633.360,4627.473,4632.374,4629.162,4622.887,4619.729,4624.471,4625.909,4637.499,4670.119,4693.372,4679.347,4669.048,4651.447,4642.121,4646.545,4649.719,4650.037,4655.438,4655.206,4645.784,4644.424,4634.488,4625.230,4617.295,4614.189,4630.330,4625.862,4615.445,4606.478,4597.543,4600.036,4586.925,4580.766,4573.511,4583.290,4582.163,4594.797,4591.802,4586.262,4582.531,4579.405,4582.100,4585.619,4598.204,4603.488,4609.921,4602.777,4595.117,4587.876,4569.131,4537.301,4523.769,4522.355,4502.563,4504.037,4517.799,4520.070,4526.600,4532.091,4532.757,4541.305,4539.932,4536.715,4528.109,4524.337,4522.334,4544.104,4548.441,4546.856,4555.181,4564.136,4562.137,4549.843,4546.139,4554.026,4555.431,4561.314,4552.261,4553.254,4549.082,4545.229,4553.516,4542.221,4539.524,4537.119,4529.574,4517.042,4495.356,4504.439,4500.886,4494.715,4504.852,4512.872,4513.947,4502.774,4496.154,4482.797,4487.544,4525.557,4526.769,4527.394,4491.173,4476.118,4473.216,4478.697,4465.275,4461.243,4472.296,4503.886,4537.356,4533.254,4531.365,4535.278,4534.915,4552.314,4564.059,4550.202,4507.823,4477.130,4478.964,4463.010,4486.058,4523.475,4522.091,4555.520,4547.192,4544.396,4522.264,4478.459,4465.447,4483.738,4481.677,4472.732,4485.893,4479.805,4458.206,4462.036,4441.991,4429.204,4390.630,4375.455,4376.371,4380.771,4365.445,4363.376,4382.028,4370.523,4389.192,4420.756,4460.482,4475.020,4507.205,4513.981,4515.525,4527.549,4511.584,4506.500,4490.791,4488.647,4488.628,4489.079,4504.555,4499.717,4489.802,4475.874,4481.728,4485.832,4482.913,4508.380,4492.531,4438.519,4417.638,4408.560,4401.125,4383.222,4375.740,4378.947,4330.845,4325.491,4344.414,4363.829,4375.795,4395.409,4405.024,4432.341,4436.809,4400.365,4395.982,4399.369,4402.652,4415.419,4402.563,4469.057]
bed_elevation = spreadsheet['Bed_elevation'].tolist()

# create a list of midpoints which will hold the flux that we calculate
midpoint_flux = [0] * (gridpoints - 1)

# create a list of widths in meters along the glacier at the gridpoints
width = (spreadsheet['WIDTH_m'] / 1000).tolist()

# surface mass balance
# an equation for the surface that drops into the negatives
def getMassBalance(i):
    precip = 2 - (i / (0.4 * gridpoints)) ** 3
    return precip


def calculateFlux():
    # loop through our midpoints by index value, 0 -> gridpoints - 1
    for i in range(gridpoints - 1):
        # get our elevation data based on our current index value
        upstream_ice_elevation = ice_elevation[i]
        downstream_ice_elevation = ice_elevation[i + 1]
        upstream_bed_elevation = bed_elevation[i]
        downstream_bed_elevation = bed_elevation[i + 1]

        # get our width data based on current index value
        upstream_width = width[i]
        downstream_width = width[i + 1]
        average_width = 0.5 * (upstream_width + downstream_width)

        # calculate our thickness values
        upstream_thickness = upstream_ice_elevation - upstream_bed_elevation
        downstream_thickness = downstream_ice_elevation - downstream_bed_elevation

        # calculate big H, our average thickness at this midpoint
        H = (upstream_thickness + downstream_thickness) / 2

        # calculate our slope, change in elevation over change in distance
        slope = (downstream_ice_elevation - upstream_ice_elevation) / dx

        # calculate diffusivity from these terms
        D = Afl * H ** (n + 2) * fabs(slope) ** (n - 1)

        # calculate flux
        flux = (
            D * slope * average_width
        )  # going to be a negative value since our slope is sloping downstream

        # set our midpoint flux at this index to our newly calculated value
        midpoint_flux[i] = flux


def calculateThickness():
    for i in range(gridpoints):
        # grab our current values based on this index
        current_ice_elevation = ice_elevation[i]
        current_bed_elevation = bed_elevation[i]
        current_upstream_width = width[i]
        current_downstream_width = width[i + 1]

        # get the upstream flux from our flux array
        #
        # so, if
        # flux = [0, 1, 2, 3, 4, ..., 123]
        # iceE = [0, 1, 2, 3, 4, ..., 123, 124]
        #
        # upstream flux = flux element at i - 1
        # downstream flux = flux element at i
        #

        # assume the first element case
        current_upstream_flux = 0

        # if we're not at the first element than we can pick upstream flux
        if i > 0:
            current_upstream_flux = midpoint_flux[i - 1]

        # for downstream, we need to make sure we're not at the last element
        # otherwise we set it to the same value as the upstream element so that
        # any flux is passthrough... shouldn't ever need that if our mass balance is right
        # and no ice ever gets to the end
        if i < gridpoints - 1:
            current_downstream_flux = midpoint_flux[i]
        else:
            current_downstream_flux = current_upstream_flux

        # get our mass balance flux
        mass_balance_flux = getMassBalance(i)

        # get average width
        current_average_width = 0.5 * (current_upstream_width + current_downstream_width)


        # calculate change in thickness, remember our fluxes are all negative
        # so we can add them together, but change the sign on the upstream on to make
        # it positive, then divide by the dx for flux but not mass balance, then multiply
        # by dt to get just the change for the small change in time
        change_in_thickness = (
            (((-1 * current_upstream_flux) + current_downstream_flux) / dx * current_average_width)
            + mass_balance_flux
        ) * dt

        # set our new ice elevation
        new_ice_elevation = current_ice_elevation + change_in_thickness

        # no go if our new ice is less than the bed
        if new_ice_elevation < current_bed_elevation:
            new_ice_elevation = current_bed_elevation

        # update our array in place
        ice_elevation[i] = new_ice_elevation


def formatOutputElements():
    out = []
    for i in range(gridpoints):
        out.append(
            {
                "iceElevation": ice_elevation[i],
                "bedElevation": bed_elevation[i],
                "diffusivity_up": 0,
                "flux_up": 0,
                "diffusivity_down": 0,
                "flux_down": 0,
                "totalFlux": 0,
                "massBalanceFlux": 0,
                "iteration": 0,
                "deltaH": 0,
            }
        )
    return out


def formatOutputMidpoints():
    out = []
    for i in range(gridpoints - 1):
        out.append(
            {
                "elementDown": 0,
                "elementUp": 0,
                "diffusivity": 0,
                "slope": 0,
                "flux": midpoint_flux[i],
            }
        )
    return out


# t should just be iteration count, run it out to a million iterations
t = 0

# we'll track model time separately
model_time = 0
start = time.time()
while t < iterations:
    t = t + 1
    calculateFlux()
    calculateThickness()

    # our modeled time is the iteration count times our dt
    model_time = t * dt  # should be in years

    # check our progress every 10 years
    if model_time % 10 == 0:
        # Now save a file out so we can view it in our webpage
        data = {
            "i": t,
            "t": model_time,
            "elements": formatOutputElements(),
            "midpoints": formatOutputMidpoints(),
        }
        outtime = int(model_time)
        outfilename = f"..\py-out/data-{outtime:04}.json"
        with open(outfilename, "w") as outfile:
            json.dump(data, outfile)
        print(t, model_time, ice_elevation[0], ice_elevation[100:105])

end = time.time()
print(f"Completed {iterations} iterations in {(end-start)/60} minutes")
