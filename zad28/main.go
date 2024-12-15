package main

import (
	"fmt"
	"math/rand/v2"
	"os"

	"cardinality.bigdata/cardinality"
)

func main() {
	// Let's estimate 1e7 cardinality
	breakPoints := map[int]bool{}

	point := 1000
	for point <= 1e7 {
		breakPoints[point] = false
		// This will add a redundant point for point == 1e7, but it does not matter
		breakPoints[5*point] = false
		point *= 10
	}

	// Neighbourhood of #registers * log(#registers)
	for i := 7090; i <= 7100; i++ {
		breakPoints[i] = false
	}

	outputFile, err := os.Create("results.csv")
	if err != nil {
		panic(err)
	}
	defer outputFile.Close()

	_, err = outputFile.WriteString("card,errHll,errLL\n")
	if err != nil {
		panic(err)
	}

	for range 30 {
		for key := range breakPoints {
			breakPoints[key] = true
		}
		hll := cardinality.NewHyperLogLog(10)
		ll := cardinality.NewLogLog(10)

		distinctElemts := make(map[uint32]struct{})
		for len(distinctElemts) <= 1e7 {
			randVal := rand.Uint32()
			distinctElemts[randVal] = struct{}{}

			hll.Add(randVal)
			ll.Add(randVal)

			if active := breakPoints[len(distinctElemts)]; active {
				breakPoints[len(distinctElemts)] = false
				card := uint64(len(distinctElemts))
				errHll := float64(hll.Count()-card) / float64(card)
				errLL := float64(ll.Count()-card) / float64(card)

				_, err := outputFile.WriteString(fmt.Sprintf("%d,%f,%f\n", len(distinctElemts), errHll, errLL))
				if err != nil {
					panic(err)
				}
			}

		}
	}
}
