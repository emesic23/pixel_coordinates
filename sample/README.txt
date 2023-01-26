mono-12540.jpq and thermal-25080.tiff should be quite similar in content. The numerical offset is because difference in camera FPS.

Important columns:
image, camNED_qx/y/z/w, camLLA_lat/lon/alt

K is intrinsics matrix of the thermal camera.
D is distortion coefficients (this is incorporated into K already) 
R is extrinsics matrix (it is identity since it assumes camera at center of coordinate frame)
P is camera projection matrix. (this combines both intrinsics and extrinsics transformation matrices)

Rough guide:
1. Rectify (undistort) thermal image using K/P (they are the same, since R is identity).
	-- Can be done using an opencv function 

2. Use quaternions camNED_qx/y/z/w to find euler angles of camera (roll, pitch yaw). Call this vector of length 3, theta.
	-- Just use a numpy or scipy library or something.   

3. Get camera information (field of view + image dimensions H, W) online. 
	-- This is needed to compute lat, lng at pixel. 
	-- Assume camera is pointed directly at the pixel in the center of the image. 
	-- Use field of view to compute angle offsets to each pixel relative to the center. 
 
3. Use altitude camLLA_alt,f orientation theta, and camera info (field-of-view + image dim.) to compute pixel lat, lng.    

4. Use the soccer field + google earth to check correctness/precision. 
	-- Soccer field lines are a bit difficult to see in thermal frame. 
	