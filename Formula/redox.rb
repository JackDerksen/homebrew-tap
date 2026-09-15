class Redox < Formula
  desc "Terminal-based, Vim-like text editor built with MinUI"
  homepage "https://github.com/JackDerksen/redox"
  url "https://github.com/JackDerksen/redox/archive/refs/tags/v0.8.1.tar.gz"
  sha256 "e6638c9273f721c1626253fca03fd8d611361c149d1e3da9b0413f676383d290"
  license "MIT"

  depends_on "rust" => :build
  uses_from_macos "curl"

  def fetch
    system "cargo", "fetch", "--locked"
  end

  def install
    system "cargo", "install", *std_cargo_args
  end

  test do
    # The first packaged release predates --version; exercise argument validation.
    assert_match "--config requires a path", shell_output("#{bin}/redox --config 2>&1", 1)
  end
end
