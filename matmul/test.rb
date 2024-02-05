# Writen by Attractive Chaos; distributed under the MIT license

def matmul(a, b)
  m = a.length
  n = a[0].length
  p = b[0].length

  # transpose
  b2 = Array.new(n) { Array.new(p) { 0 } }
  n.times do |i|
    p.times do |j|
      b2[j][i] = b[i][j]
    end
  end

  # multiplication
  c = Array.new(m) { Array.new(p) { 0 } }
  m.times do |i|
   p.times do |j|
      s = 0
      ai, b2j = a[i], b2[j]
      n.times do |k|
        s += ai[k] * b2j[k]
      end
      c[i][j] = s
    end
  end
  c
end

def matgen(n)
  tmp = 1.0 / n / n
  a = Array.new(n) { Array.new(n) { 0 } }
  n.times do |i|
    n.times do |j|
      a[i][j] = tmp * (i - j) * (i + j)
    end
  end
  a
end

def run(n)
  t = Time.now
  n = n / 2 * 2
  a = matgen(n)
  b = matgen(n)
  c = matmul(a, b)
  puts "%.9f" % c[n/2][n/2]

  STDERR.puts("time(#{Time.now - t})")
end

n = (ARGV[0] || 10).to_i
times = (ARGV[1] || 1).to_i
STDERR.puts("started\t#{Process.pid}")
times.times { run(n) }
