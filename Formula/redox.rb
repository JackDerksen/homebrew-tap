class Redox < Formula
  desc "Terminal-based, Vim-like text editor built with MinUI"
  homepage "https://github.com/JackDerksen/redox"
  url "https://github.com/JackDerksen/redox/archive/refs/tags/v0.9.1.tar.gz"
  sha256 "2c479ca8906b0c99d431368ef4fef6c3c2e7d5cae25285146c1f0a0380209235"
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
