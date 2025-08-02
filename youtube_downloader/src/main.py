import argparse
from pathlib import Path

from pytubefix import YouTube
from pytubefix.exceptions import VideoUnavailable
from tqdm import tqdm


class YouTubeDownloader:
  """A class to download YouTube videos with a progress bar."""

  def __init__(self, url, output_path=None, quality=None):
    """
    Initializes the YouTubeDownloader with the given URL, output path, and quality.

    Args:
      url: The URL of the YouTube video.
      output_path: The directory to save the downloaded video. Defaults to the current working directory.
      quality: The desired video quality (e.g., 'highest', 'lowest', '720p'). Defaults to 'highest'.
    """
    if output_path is None:
      # Set output_path to the current working directory if not provided
      self.output_path = Path.cwd()
    else:
      # Ensure output_path is a Path object
      self.output_path = Path(output_path)

    self.url = url
    self.quality = quality
    # Initialize YouTube object with progress and complete callbacks
    self.yt = YouTube(
        self.url,
        on_progress_callback=self.progress_function,
        on_complete_callback=self.complete_function
    )
    self.pbar = None

  def download(self):
    """
    Downloads the YouTube video based on the initialized parameters.
    """
    try:
      # Check if the video is available
      self.yt.check_availability()
    except VideoUnavailable:
      print(f"Video '{self.url}' is unavailable.")
      return

    stream = None
    # Select the appropriate stream based on the requested quality
    if self.quality == "highest":
      stream = self.yt.streams.filter(progressive=True,
                                      file_extension="mp4"
                                      ).get_highest_resolution()
    elif self.quality == "lowest":
      stream = self.yt.streams.filter(progressive=True,
                                      file_extension="mp4"
                                      ).get_lowest_resolution()
    else:
      # Attempt to find a stream with the requested resolution
      stream = self.yt.streams.filter(
          progressive=True,
          file_extension='mp4',
          res=self.quality
      ).first()

      # If no stream found for the requested quality, fallback to highest resolution
      if stream is None:
        print(f"Requested quality '{self.quality}' not available. Downloading highest resolution instead.")
        stream = self.yt.streams.filter(progressive=True,
                                        file_extension="mp4"
                                        ).get_highest_resolution()

    # Initialize tqdm progress bar if a stream was found
    if stream:
      self.pbar = tqdm(
          total=stream.filesize,
          unit="B",
          unit_scale=True,
          desc=self.yt.title,
      )
      # Download the selected stream
      stream.download(output_path=self.output_path)
    else:
        print("Could not find a suitable stream to download.")


  def progress_function(self, stream, chunk, bytes_remaining):
    """
    Callback function to update the progress bar during download.

    Args:
      stream: The stream being downloaded.
      chunk: The downloaded chunk of data.
      bytes_remaining: The number of bytes remaining to download.
    """
    current = stream.filesize - bytes_remaining
    # Update the progress bar with the difference between current progress and previous progress
    self.pbar.update(current - self.pbar.n)


  def complete_function(self, stream, file_path):
    """
    Callback function to close the progress bar and print a success message after download.

    Args:
      stream: The stream that was downloaded.
      file_path: The path where the video was saved.
    """
    # Close the progress bar
    self.pbar.close()
    print(f"\nDownloaded '{self.yt.title}' successfully to {file_path}")


if __name__ == "__main__":
  # Set up argument parser for command-line usage
  parser = argparse.ArgumentParser(description="YouTube Downloader")

  # Add arguments
  parser.add_argument("url", help="YouTube video URL")
  parser.add_argument("-q", "--quality", help="Video Quality", default="highest")
  parser.add_argument("-o", "--output_path", help="Output directory", default=None)

  # Parse command-line arguments
  args = parser.parse_args()

  # Create a YouTubeDownloader instance and start the download
  downloader = YouTubeDownloader(args.url, args.output_path, args.quality)
  downloader.download()