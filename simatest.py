import sima
import sima.motion

sequences = [sima.Sequence.create('TIFF', "C:\Users\hakan\Documents\git_repos\Munich_sample_FR1_FFT_16.tif")]
#dataset = sima.ImagingDataset(sequences, "C:\Users\hakan\Documents\git_repos\Munich_sample_FR1_FFT.sima")

mc_approach = sima.motion.PlaneTranslation2D(max_displacement=[15, 30])
dataset = mc_approach.correct(sequences, "C:\Users\hakan\Documents\git_repos\Munich_sample_FR1_FFT_16.sima")

dataset.export_frames([[['C:\Users\hakan\Documents\git_repos\\frames.tif']]], fmt='TIFF16')
