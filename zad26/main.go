package main

import (
	"fmt"
	"math"
	"math/big"
	"os"
)

// Helper function to calculate the binomial coefficient (n choose k) using math/big
func binomialCoefficient(n, k int) *big.Int {
	if k > n {
		return big.NewInt(0)
	}
	if k == 0 || k == n {
		return big.NewInt(1)
	}

	num := big.NewInt(1)
	den := big.NewInt(1)
	for i := 1; i <= k; i++ {
		num.Mul(num, big.NewInt(int64(n-i+1)))
		den.Mul(den, big.NewInt(int64(i)))
	}

	result := big.NewInt(0)
	result.Div(num, den)
	return result
}

// snExact calculates Sn exactly using math/big for arbitrary-precision integers
func snExact(n int) float64 {
	sumVal := big.NewFloat(0.0)
	powTwoN := new(big.Float).SetFloat64(math.Pow(2, float64(n)))

	for k := 0; k <= n; k++ {
		binCoeff := new(big.Float).SetInt(binomialCoefficient(n, k))
		term := new(big.Float).SetFloat64(math.Sqrt(float64(k * (n - k))))
		binCoeff.Mul(binCoeff, term)
		sumVal.Add(sumVal, binCoeff)
	}

	snExactResult := new(big.Float).Quo(sumVal, powTwoN)
	result, _ := snExactResult.Float64()
	return result
}

// snApprox calculates the delta method approximation of Sn
func snApprox(n int) float64 {
	return float64(n)/2 - 0.25
}

func main() {
	file, err := os.CreateTemp("", "")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	file.WriteString("Aprox,Exact\n")

	for n := 1; n <= 100; n++ {
		aprox := snApprox(n)
		exact := snExact(n)
		_, err := file.WriteString(fmt.Sprintf("%f,%f\n", aprox, exact))
		if err != nil {
			panic(err)
		}
	}

	fmt.Println(file.Name())
}
