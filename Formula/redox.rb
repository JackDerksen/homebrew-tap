class Redox < Formula
  desc "Terminal-based, Vim-like text editor built with MinUI"
  homepage "https://github.com/JackDerksen/redox"
  url "https://github.com/JackDerksen/redox/archive/refs/tags/v0.10.0.tar.gz"
  sha256 "418adbc688c18266e702e9266a7f622971fe38fe8f308a82856655c64192ae19"
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
