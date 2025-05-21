-- AGX Tonemapper Client-Side Script

if SERVER then
    -- This script should only run on the client
    return
end

local agx_material_path = "materials/agx_tonemap.vmt"
local agx_tonemap_material -- Will store our created material

-- Attempt to create the material when the script loads
-- The VMT file (agx_tonemap.vmt) should define:
-- "UnlitGeneric" {
--     "$basetexture" "_rt_FullFrameFB"
--     "$pixshader" "agx_pixel_shader"
--     "$nocull" 1
--     "$vertexalpha" 1
--     "$vertexcolor" 1
-- }
-- So, CreateMaterial only needs a unique name and the VMT path.
agx_tonemap_material = CreateMaterial("agx_tonemap_material_unique_name", agx_material_path, "UnlitGeneric")

if not agx_tonemap_material or agx_tonemap_material:IsErrorMaterial() then
    ErrorNoHalt("AGX Tonemapper: Failed to create material! Path: " .. agx_material_path .. "\n")
    if agx_tonemap_material then
        ErrorNoHalt("AGX Tonemapper: Material error: " .. agx_tonemap_material:GetError() .. "\n")
    end
    agx_tonemap_material = nil -- Ensure we don't try to use an error material
else
    -- Ensure basetexture is correctly set if not implicitly handled by VMT loading in CreateMaterial
    -- For shaders using _rt_FullFrameFB, it's often implicitly available.
    -- However, explicitly setting it can sometimes resolve issues if the VMT isn't perfectly processed.
    -- agx_tonemap_material:SetTexture("$basetexture", render.GetFullFrameFrameBuffer())
    -- For this task, we assume the VMT correctly sets $basetexture to _rt_FullFrameFB
    -- and $pixshader to agx_pixel_shader.
    -- No dynamic parameters need to be set for this version as they are hardcoded in the shader.
end

hook.Add("RenderScreenspaceEffects", "AGXTonemapperEffect", function()
    if not agx_tonemap_material or agx_tonemap_material:IsErrorMaterial() then
        -- Attempt to recreate material if it was missing or errored previously
        if not agx_tonemap_material then
            agx_tonemap_material = CreateMaterial("agx_tonemap_material_unique_name", agx_material_path, "UnlitGeneric")
            if not agx_tonemap_material or agx_tonemap_material:IsErrorMaterial() then
                -- Still failing, print error once to avoid spam
                if not agx_tonemap_material or not agx_tonemap_material.loggedError then
                    ErrorNoHalt("AGX Tonemapper: Material still invalid in RenderScreenspaceEffects. Disabling effect.\n")
                    if agx_tonemap_material then agx_tonemap_material.loggedError = true end
                end
                return -- Do not proceed with rendering
            else
                 -- Material successfully created this time
            end
        else -- Was an error material
            ErrorNoHalt("AGX Tonemapper: Material previously errored. Disabling effect.\n")
            return
        end
    end

    -- At this point, agx_tonemap_material should be valid.

    -- The VMT should handle setting "$basetexture" to "_rt_FullFrameFB"
    -- and "$pixshader" to "agx_pixel_shader".
    -- Shader parameters (matrix, EV values, etc.) are hardcoded in the .psh file.

    -- Apply the tonemapping effect
    render.SetMaterial(agx_tonemap_material)
    render.DrawScreenQuad()

    -- Note: render.UpdateScreenEffectTexture() is not strictly needed here if
    -- we are using _rt_FullFrameFB which is already the result of the main scene render.
    -- If we were to use GetScreenEffectTexture(0), we would call UpdateScreenEffectTexture() before it.
end)

print("AGX Tonemapper: Client script loaded and hook added.")
