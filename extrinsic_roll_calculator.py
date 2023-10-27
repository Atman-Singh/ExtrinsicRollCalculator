import numpy as np
import math

def main():

    # user inputs yaw and pitch from cad
    yaw = float(input('Yaw (degrees): '))
    pitch = float(input('Pitch (degrees): '))
    
    # create transformation matrices: apply yaw -> rotate onto z-axis -> apply pitch -> rotate back
    yaw_transformation = yaw_matrix(yaw)
    z_axis_align_transformation = yaw_matrix(90-yaw)
    pitch_transformation = pitch_matrix(pitch)
    z_axis_realign_transformation = yaw_matrix(-(90-yaw))

    # apply transformations to arbitrary vector [0, 0, 1]
    transformations = [yaw_transformation, z_axis_align_transformation, pitch_transformation, z_axis_realign_transformation]
    initial_line_of_sight = np.array([0, 0, 1])
    final_line_of_sight = transform_vector(transformations, initial_line_of_sight)

    # get roll angle from final line of sight to xy plane
    radius = math.sqrt(1-math.pow(final_line_of_sight[2], 2))
    flat_line_of_sight = [radius, 0, final_line_of_sight[2]]
    extrinsic_roll = math.degrees(math.acos(final_line_of_sight[0]/flat_line_of_sight[0]))

    # print result
    print('Extrinsic role:', extrinsic_roll)
 
# creates transformation matrix that rotates rigid body about y-axis
def yaw_matrix(angle):
    return np.array([[math.cos(angle), 0, math.sin(angle)],
                    [0, 1, 0],
                    [-math.sin(angle), 0, math.cos(angle)]])

# creates transformation matrix that rotates rigid body about x-axis
def pitch_matrix(angle):
    return np.array([[math.cos(angle), -math.sin(angle), 0],
                    [math.sin(angle), math.cos(angle), 0],
                    [0, 0, 1]])

# applies list of transformations to a vector
def transform_vector(transformations, vector):
    for transformation in transformations:
        vector = np.matmul(vector, transformation)
    return vector

if __name__ == '__main__':
    main()