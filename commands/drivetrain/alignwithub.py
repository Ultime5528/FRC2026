import math


from subsystems.drivetrain import Drivetrain
from wpimath.geometry import Pose2d, Translation2d, Rotation2d


from ultime.command import DeferredCommand

shooter_offset1 = Translation2d(0,0)
shooter_edge = Translation2d(1,0)

def computeRobotRotationToAlign(robot_pose2d: Pose2d, shooter_offset: Translation2d, shooter_extremity: Translation2d, hubpose: Pose2d) -> Rotation2d:

    delta_hub_and_bot = hubpose.translation()-robot_pose2d.translation()
    hub_at_origin = delta_hub_and_bot.rotateBy(-robot_pose2d.rotation())
    shooter_direction = shooter_extremity - shooter_offset

    #should use shooter_direction.cross(hub_at_origin) in 2026
    A = shooter_direction.x*hub_at_origin.y-shooter_direction.y*hub_at_origin.x
    #should use shooter_direction.dot(hub_at_origin) in 2026
    B = shooter_direction.x*hub_at_origin.x+shooter_direction.y*hub_at_origin.y
    #should use shooter_offset.cross(shooter_extremity)
    C = shooter_offset.x*shooter_extremity.y-shooter_offset.y*shooter_extremity.x

    return Rotation2d(math.atan2(-B,-A) + math.acos(C/((A**2)+(B**2))))

class AlignWithHub(DeferredCommand):
    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self.drivetrain = drivetrain
        self.addRequirements(drivetrain)

    def initialize(self):
        #self.first_rotation2d = self.drivetrain._gyro.getRotation2d()
        #self.align_rotation2d = computeRobotRotationToAlign(self.drivetrain.getPose(),shooter_offset1.translation(),shooter_edge.translation(), Pose2d(2,2,0))
        pass

    def execute(self):
        self.drivetrain.driveRaw(0,0,0.8, False)
        print(self.drivetrain.getGyroAngle())


    def isFinished(self) -> bool:
        align_rotation2d = computeRobotRotationToAlign(self.drivetrain.getPose(),shooter_offset1,shooter_edge, Pose2d(0.01,0.01,0))
        return abs(align_rotation2d.degrees()) < 1.0
        #return self.move_by <= self.drivetrain._gyro.getRotation2d()-self.first_angle

    def end(self, interrupted):
        pass










