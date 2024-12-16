package cardinality

import (
	"math"
	"math/bits"
)

type HyperLogLog struct {
	alpha       float64
	registers   []uint8
	precision   uint32
	addressMask uint32
}

func NewHyperLogLog(precision uint32) *HyperLogLog {
	if precision < 4 || precision > 16 {
		panic("invalid precision")
	}

	return &HyperLogLog{
		alpha:       selectAlphaHll(precision),
		registers:   make([]uint8, 1<<precision),
		precision:   precision,
		addressMask: selectAddressMaskHll(precision),
	}
}

func (h *HyperLogLog) Add(hash uint32) {
	index := h.addressMask & hash
	trailing := hash >> h.precision
	// Position of the first 1
	bitPos := bits.TrailingZeros32(trailing) + 1
	if bitPos == 33 {
		bitPos = 33 - int(h.precision)
	}
	// Note: BitPos is in [0,33]
	if h.registers[index] < uint8(bitPos) {
		h.registers[index] = uint8(bitPos)
	}

}

func (h *HyperLogLog) Count() uint64 {
	var harmonicMean float64
	var numOfZeroes uint64
	for _, reg := range h.registers {
		harmonicMean += 1.0 / float64(uint64(1<<reg))
		if reg == 0 {
			numOfZeroes++
		}
	}
	harmonicMean = 1.0 / harmonicMean

	m := float64(uint64(1 << h.precision))
	rawEstimate := h.alpha * m * m * harmonicMean

	if rawEstimate <= 2.5*m {
		// Low range correction
		if numOfZeroes != 0 {
			return uint64(m * math.Log(m/float64(numOfZeroes)))
		}
		return uint64(rawEstimate)
	} else if rawEstimate <= 1.0/30.0*math.Pow(2, 32) {
		// Mid range, no correction
		return uint64(rawEstimate)
	}

	// High range correction
	return -uint64(math.Pow(2, 32) * math.Log(1-rawEstimate/math.Pow(2, 32)))
}

func selectAlphaHll(precision uint32) float64 {
	var result float64
	switch precision {
	case 4:
		result = .673
	case 5:
		result = .697
	case 6:
		result = .709
	default:
		m := float64(uint32(0x1) << precision)
		result = 0.7213 / (1 + 1.079/m)
	}

	return result
}

func selectAddressMaskHll(precision uint32) uint32 {
	return (0xFFFF) >> (16 - precision)
}
