package cardinality

import (
	"math"
	"math/bits"
)

type LogLog struct {
	alpha       float64
	registers   []uint8
	precision   uint32
	addressMask uint32
}

func NewLogLog(precision uint32) *LogLog {
	if precision < 4 || precision > 16 {
		panic("invalid precision")
	}

	return &LogLog{
		alpha:       selectAlphaLl(precision),
		registers:   make([]uint8, 1<<precision),
		precision:   precision,
		addressMask: selectAddressMaskLl(precision),
	}
}

func (l *LogLog) Add(hash uint32) {
	index := l.addressMask & hash
	trailing := hash >> l.precision
	// Position of the first 1
	bitPos := bits.TrailingZeros32(trailing) + 1
	newVal := l.registers[index]
	// Note: BitPos is in [0,33]
	if newVal < uint8(bitPos) {
		newVal = uint8(bitPos)
	}
	l.registers[index] = newVal
}

func (l *LogLog) Count() uint64 {
	m := float64(uint64(1) << l.precision)
	var geoMean float64
	for _, reg := range l.registers {
		geoMean += float64(reg)
	}
	geoMean /= m
	geoMean = math.Pow(2.0, geoMean)

	return uint64(l.alpha * m * geoMean)
}

func selectAlphaLl(precision uint32) float64 {
	m := float64(uint64(1) << precision)
	return math.Gamma((-1 / m)) * (1 - math.Pow(2, 1/m)) / math.Log(2)
}

func selectAddressMaskLl(precision uint32) uint32 {
	return (0xFFFF) >> (16 - precision)
}
