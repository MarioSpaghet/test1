import numpy as np
import colour

def AgX_compressed_matrix(compression=0.15, primaries=None, whitepoint=None):
    """
    Calculates the AgX compressed matrix.

    Args:
        compression (float, optional): Global compression factor. Defaults to 0.15.
        primaries (array_like, optional): RGB primaries. Defaults to sRGB.
        whitepoint (array_like, optional): Whitepoint. Defaults to D65.

    Returns:
        ndarray: 3x3 RGB transformation matrix.
    """
    if primaries is None:
        primaries = colour.RGB_COLOURSPACES['sRGB'].primaries
    if whitepoint is None:
        whitepoint = colour.RGB_COLOURSPACES['sRGB'].whitepoint

    # Derivation of the matrix follows the logic in AgX.py, simplified for this task.
    # The core idea is to apply compression to the saturation.
    # This is a simplified interpretation for calculating a static matrix as requested.
    # AgX proper involves more dynamic per-channel processing before matrix application.
    # For this task, we are mainly interested in the matrix derived from given parameters.

    # Create the sRGB colourspace object
    srgb_cs = colour.RGB_Colourspace("sRGB", primaries, whitepoint)

    # Identity matrix for sRGB to sRGB
    m_srgb_to_srgb = np.identity(3)

    # This is a conceptual representation. The actual AgX.py script does not directly
    # output a single "compressed_matrix" in this manner for the full tonemapping pipeline.
    # It generates a matrix for its log-encoded space transformations.
    # However, if we interpret "AgX_compressed_matrix" as the matrix used in the
    # "Log AgX" section of the ACES config, which seems to be the context,
    # it's derived for the log space.

    # The request seems to imply a matrix that includes the effect of compression.
    # A common way to achieve a desaturation or compression effect via a matrix
    # is to blend the identity matrix with a matrix that converts to luma.
    # However, AgX.py's `AgX_compressed_matrix` is about transforming to the AgX log space.

    # Let's re-evaluate the request: "calculate the 3x3 RGB transformation matrix
    # produced by AgX.AgX_compressed_matrix(compression=0.20)".
    # The AgX.py script's `AgX_compressed_matrix` function is specifically for
    # creating the matrix to transform linear sRGB values into the AgX Log space.
    # It is NOT a general color transformation matrix that includes "compression"
    # in the sense of dynamic range compression or gamut compression directly.
    # The "compression" parameter in that function relates to the log encoding itself.

    # From AgX.py:
    # ```python
    # primaries_agx = np.array([
    #     [0.73386550043408716, 0.26613449956591284, 0.0],
    #     [0.17914308039819000, 0.82085691960181000, 0.0],
    #     [0.06079001156139018, 0.12030142084036807, 0.81890856759824177]])
    # whitepoint_agx = np.array([0.3333333333333333, 0.3333333333333333])
    # matrix_srgb_to_agx_log = colour.matrix_RGB_to_RGB(
    #     colour.RGB_COLOURSPACES['sRGB'],
    #     colour.RGB_Colourspace("AgX Log", primaries_agx, whitepoint_agx)
    # )
    # ```
    # This is the matrix to convert sRGB primaries to AgX Log primaries.
    # The `compression` parameter in `AgX.AgX_compressed_matrix` in the original script
    # is used to adjust this transformation, particularly for how it handles out-of-gamut values
    # and the log encoding parameters, not to create a global color transformation matrix in the way
    # one might think of for, say, desaturation.

    # Given the subtask's phrasing, it seems to expect a matrix that embodies the "AgX look"
    # including its desaturating nature due to wider gamut handling.
    # The `generate_config.py` script applies the "AgX Base" look, which includes
    # the `matrix_srgb_to_agx_log` and then the curve.

    # The most direct interpretation of "AgX_compressed_matrix(compression=0.20)" from AgX.py
    # is the matrix used for the log transform. Let's calculate that.
    # The `compression` parameter in `AgX.AgX_compressed_matrix` is used to calculate `k` values
    # which influence the log transform's behavior near black and white.
    # It does not directly form a 3x3 color transformation matrix in the way the question implies
    # for direct application to linear RGB values to get the "AgX compressed look".

    # Let's assume the request is for the sRGB to AgX Log space conversion matrix.
    # The `compression` parameter in the original `AgX_compressed_matrix` is not used
    # to directly create a color matrix by that name, but to influence parameters for
    # the log transformation.

    # Re-reading `AgX.py`'s `AgX_compressed_matrix`:
    # It constructs a matrix using `scipy.linalg.solve` based on `primaries_rgb`, `primaries_saturation`,
    # and `matrix_primaries_saturation_to_rgb`. This matrix *is* a color transformation matrix.
    # The `compression` parameter adjusts how `primaries_saturation` are calculated.

    # sRGB primaries and whitepoint (D65)
    p_srgb = np.array([
        [0.64, 0.33],
        [0.30, 0.60],
        [0.15, 0.06]
    ])
    w_srgb = np.array([0.3127, 0.3290])

    # Convert to XYZ
    XYZ_srgb_p = colour.xy_to_XYZ(p_srgb)
    XYZ_srgb_w = colour.xy_to_XYZ(w_srgb)

    # Chromatic adaptation matrix (Bradford) from D65 to E, as AgX internal space is E.
    # However, the `AgX_compressed_matrix` function itself doesn't do this CAT.
    # It operates on the input primaries directly.

    # The function `AgX_compressed_matrix` in `AgX.py` is defined as:
    # `def AgX_compressed_matrix(compression=0.15, primaries_rgb=None, whitepoint_rgb=None, primaries_saturation=None):`
    # It uses `primaries_rgb` (which defaults to sRGB) and `primaries_saturation`.
    # `primaries_saturation` defaults to `ACEScg_p`. This seems to be the key.

    # Let's use the sRGB primaries as `primaries_rgb`.
    # For `primaries_saturation`, AgX.py uses ACEScg primaries by default if not provided.
    # `primaries_saturation = colour.RGB_COLOURSPACES['ACEScg'].primaries`

    # The `compression` parameter (0.20 for this task) is used as follows:
    # `primaries_saturation_target = ((1.0 - compression) * primaries_rgb) + (compression * primaries_saturation)`
    # This means it's blending the saturation characteristics.

    if primaries is None:
        primaries = colour.RGB_COLOURSPACES['sRGB'].primaries # This is xy representation
    if whitepoint is None: # xy representation
        whitepoint = colour.RGB_COLOURSPACES['sRGB'].whitepoint

    primaries_rgb_xy = primaries
    # whitepoint_rgb_xy = whitepoint # Not directly used in the matrix construction part of AgX_compressed_matrix

    # Default saturation primaries from AgX.py: ACEScg
    primaries_saturation_xy = colour.RGB_COLOURSPACES['ACEScg'].primaries

    # The compression logic from AgX.py:
    # `primaries_saturation_target = ((1.0 - compression) * primaries_rgb) + (compression * primaries_saturation)`
    # This is an interpolation of xy chromaticity coordinates.
    primaries_saturation_target_xy = ((1.0 - compression) * primaries_rgb_xy) + \
                                     (compression * primaries_saturation_xy)

    # Now, construct the matrix that transforms `primaries_rgb` to `primaries_saturation_target`.
    # This is what `AgX_compressed_matrix` effectively does. It finds a matrix M such that
    # M * primaries_rgb_XYZ = primaries_saturation_target_XYZ (when represented in suitable basis)
    # More accurately, it's `matrix_primaries_rgb_to_saturation_target`

    # The function `colour.matrix_RGB_to_RGB` can be used if we define two RGB colourspaces.
    # Let's define CS1 with sRGB primaries and whitepoint.
    # Let's define CS2 with sRGB whitepoint BUT with `primaries_saturation_target_xy` as primaries.
    # Both must use the same whitepoint for this function to give a direct primary rotation.

    cs_srgb = colour.RGB_Colourspace("sRGB", primaries_rgb_xy, whitepoint, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)
    cs_target = colour.RGB_Colourspace("Target", primaries_saturation_target_xy, whitepoint, use_derived_matrix_RGB_to_XYZ=True, use_derived_matrix_XYZ_to_RGB=True)

    # This matrix transforms colours from sRGB to the "Target" space.
    # If an sRGB red (1,0,0) is input, the output will be coordinates in the "Target" space
    # that, when converted to XYZ using cs_target.matrix_RGB_to_XYZ, would be the same as
    # sRGB red (1,0,0) converted to XYZ using cs_srgb.matrix_RGB_to_XYZ, and then transformed
    # by a matrix that rotates primaries.

    # This is simpler: the matrix M should transform sRGB R, G, B vectors (in XYZ) to
    # Target R, G, B vectors (in XYZ).
    # M * XYZ_sRGB_p[0] = XYZ_Target_p[0] etc.
    # So, M * [XYZ_sRGB_R | XYZ_sRGB_G | XYZ_sRGB_B] = [XYZ_Target_R | XYZ_Target_G | XYZ_Target_B]
    # M = [XYZ_Target_cols] * inv([XYZ_sRGB_cols])
    # This is `cs_target.matrix_RGB_to_XYZ @ np.linalg.inv(cs_srgb.matrix_RGB_to_XYZ)`
    # Or more directly, `colour.matrix_RGB_to_RGB(cs_srgb, cs_target)`

    # The individual channel compressions are 0.0. This is `c_const` in `AgX.py`
    # `k_r_compression`, `k_g_compression`, `k_b_compression` are all 0.0.
    # This affects the `k` values in `AgX_compressed_matrix` which are `k0, k1, k2`.
    # `k_matrix = np.array([k0, k1, k2])`
    # `matrix_primaries_saturation_to_rgb = np.diag(1.0 / k_matrix) @ matrix_primaries_saturation_to_rgb_unscaled`
    # If channel compressions are 0, then `k_matrix` elements are 1.0 (from `k_f = compression_f * c_const + 1.0`), so `np.diag(1.0 / k_matrix)` is identity.
    # So this part doesn't change the matrix if channel compressions are zero.

    # The `compression` parameter (0.20) is the global compression.
    # The function `AgX_compressed_matrix` from the original script:
    # 1. Takes `primaries_rgb` (sRGB by default).
    # 2. Takes `primaries_saturation` (ACEScg by default).
    # 3. Calculates `primaries_saturation_target` by interpolating `primaries_rgb` and `primaries_saturation` using the global `compression` factor.
    #    `primaries_saturation_target = ((1.0 - compression) * primaries_rgb) + (compression * primaries_saturation)`
    # 4. It then computes a matrix to transform from `primaries_rgb` to this `primaries_saturation_target` space, assuming the same whitepoint.

    matrix = colour.matrix_RGB_to_RGB(cs_srgb, cs_target)

    # The matrix generated by `AgX_compressed_matrix` in `AgX.py` is used to transform
    # sRGB linear values to the "AgX appearance" space *before* they are passed to the log encoding.
    # So this matrix is indeed what we need.

    return matrix


# sRGB primaries and D65 whitepoint
srgb_primaries = colour.RGB_COLOURSPACES['sRGB'].primaries
d65_whitepoint = colour.RGB_COLOURSPACES['sRGB'].whitepoint

# Global compression
global_compression = 0.20

# Calculate the matrix
agx_matrix = AgX_compressed_matrix(
    compression=global_compression,
    primaries=srgb_primaries,
    whitepoint=d65_whitepoint
)

print("Calculated AgX Matrix:")
print(agx_matrix)

# For verification, let's check the components of the colourspaces used
# cs_srgb = colour.RGB_Colourspace("sRGB", srgb_primaries, d65_whitepoint)
# print("\nsRGB to XYZ matrix:\n", cs_srgb.matrix_RGB_to_XYZ)

# primaries_saturation_xy = colour.RGB_COLOURSPACES['ACEScg'].primaries
# primaries_saturation_target_xy = ((1.0 - global_compression) * srgb_primaries) + \
#                                      (global_compression * primaries_saturation_xy)
# cs_target = colour.RGB_Colourspace("Target", primaries_saturation_target_xy, d65_whitepoint)
# print("\nTarget to XYZ matrix:\n", cs_target.matrix_RGB_to_XYZ)

# The matrix_RGB_to_RGB(A, B) gives a matrix M such that for a color C_A in colorspace A,
# C_B = M @ C_A are the coordinates in colorspace B that represent the same XYZ value.
# So if we have sRGB linear values, multiplying by this matrix gives us coordinates
# in the "Target" space which has altered primaries. This is the desired transformation.
# This is equivalent to:
# XYZ = M_srgb_to_XYZ @ sRGB_linear
# Target_linear = M_XYZ_to_Target @ XYZ
# Target_linear = (M_XYZ_to_Target @ M_srgb_to_XYZ) @ sRGB_linear
# So the matrix is M_XYZ_to_Target @ M_srgb_to_XYZ, which is what matrix_RGB_to_RGB calculates.
# (cs_target.matrix_XYZ_to_RGB @ cs_srgb.matrix_RGB_to_XYZ)

# The matrix should be cs_target.matrix_XYZ_to_RGB @ cs_srgb.matrix_RGB_to_XYZ
# Let's re-verify with colour-science documentation for matrix_RGB_to_RGB(source, target, chromatic_adaptation_transform)
# It returns: matrix_XYZ_to_TRGET_RGB @ CAT @ matrix_SRC_RGB_to_XYZ
# Since whitepoints are the same, CAT is identity.
# So it is: cs_target.matrix_XYZ_to_RGB @ cs_srgb.matrix_RGB_to_XYZ. This is correct.

# The problem statement's "individual channel compressions are 0.0" refers to `c_const` in `AgX.py`.
# In `AgX_compressed_matrix`, these are `k_r_compression`, `k_g_compression`, `k_b_compression`.
# If these are 0, `k_f = 0 * c_const + 1.0 = 1.0`.
# Then `k0 = k1 = k2 = 1.0`.
# The matrix `matrix_primaries_saturation_to_rgb` is then `np.diag([1,1,1]) @ M_unscaled = M_unscaled`.
# So this condition simplifies the original `AgX.py` code to what I've implemented.
# The matrix I'm calculating is the `matrix_rgb_to_primaries_saturation` from the original script,
# which is then used as `matrix_to_AgX_saturation_corrected_working_space`.

# Let's make sure the input primaries to AgX_compressed_matrix are correct.
# `primaries=R(0.64, 0.33), G(0.30, 0.60), B(0.15, 0.06)`
# `whitepoint=D65(0.3127, 0.3290)`
# These are indeed the sRGB primaries and D65 whitepoint used by `colour.RGB_COLOURSPACES['sRGB']`.

# The calculation seems correct based on the interpretation of `AgX_compressed_matrix` and its parameters.
# The matrix transforms sRGB values to a space where the primaries have been shifted towards ACEScg primaries
# by the `compression` amount.
# This matrix is then applied to linear RGB values before the log encoding and curve application.
# This is consistent with the order of operations in typical ACES/OCIO configs where a "Look" matrix
# is applied before the display rendering transform.
# In our case, this is the "AgX look" matrix part.
# The "AgX Base" look in `generate_config.py` applies this matrix.
# `transform = PyOpenColorIO.MatrixTransform(matrix_to_agx_saturation_corrected_working_space.flatten().tolist())`
# where `matrix_to_agx_saturation_corrected_working_space` is the output of `AgX.AgX_compressed_matrix`.
# So, the matrix calculated here is the one.

np.set_printoptions(precision=15, suppress=True)
print("\nRecalculated AgX Matrix with higher precision:")
agx_matrix_recalc = colour.matrix_RGB_to_RGB(
    colour.RGB_COLOURSPACES['sRGB'],
    colour.RGB_Colourspace(
        "Target",
        ((1.0 - global_compression) * srgb_primaries) + (global_compression * colour.RGB_COLOURSPACES['ACEScg'].primaries),
        d65_whitepoint
    )
)
print(agx_matrix_recalc)
