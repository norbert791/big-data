package main

import (
	"fmt"
	"math"
	"math/big"
	"os"
)

// Helper function to calculate the multinomial coefficient
func multinomialCoefficient(n, n1, n2, n3 int) *big.Int {
	if n1 < 0 || n2 < 0 || n3 < 0 || n1+n2+n3 != n {
		return big.NewInt(0)
	}

	coeff := new(big.Int).Set(binomialCoefficient(n, n1))
	coeff.Mul(coeff, binomialCoefficient(n-n1, n2))
	return coeff
}

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

// calculateTn calculates Tn exactly using math/big for arbitrary-precision integers
func calculateTn(n int) float64 {
	totalSum := big.NewFloat(0.0)
	powThreeN := new(big.Float).SetFloat64(math.Pow(3, float64(n)))

	for n1 := 0; n1 <= n; n1++ {
		for n2 := 0; n2 <= n-n1; n2++ {
			n3 := n - n1 - n2
			coeff := new(big.Float).SetInt(multinomialCoefficient(n, n1, n2, n3))
			term := new(big.Float).SetFloat64(math.Sqrt(float64(n1 * n2 * n3)))
			coeff.Mul(coeff, term)
			totalSum.Add(totalSum, coeff)
		}
	}

	tnExactResult := new(big.Float).Quo(totalSum, powThreeN)
	result, _ := tnExactResult.Float64()
	return result
}

// approximateTn calculates the delta method approximation of Tn
func approximateTn(n int) float64 {
	return math.Pow(float64(n), 1.5)/(3*math.Sqrt(3)) - math.Sqrt(3*float64(n))/4
}

func main() {
	file, err := os.CreateTemp("", "")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	file.WriteString("Aprox,Exact\n")

	for n := 1; n <= 100; n++ {
		aprox := approximateTn(n)
		exact := calculateTn(n)
		_, err := file.WriteString(fmt.Sprintf("%f,%f\n", aprox, exact))
		if err != nil {
			panic(err)
		}
	}

	fmt.Println(file.Name())
}
