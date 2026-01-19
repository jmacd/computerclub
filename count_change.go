package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
)

// For mesauring time complexity.
var steps = 0;

// This function parses the input, for example
//
//   go run ./count_change.go 100 5 10 25
//
// asks how many ways to make 100 cents with 5, 10, and 25 cent coins
func main() {
	var coins []int
	total, err := strconv.ParseUint(os.Args[1], 10, 64)
	if err != nil {
		fmt.Println("invalid total", os.Args[1])
		return
	}
	number := int(total)
	for _, arg := range os.Args[2:] {
		cents, err := strconv.ParseUint(arg, 10, 64)
		if err != nil {
			fmt.Println("invalid denomination", arg)
			return
		}
		fmt.Println("with denomination", cents)
		coins = append(coins, int(cents))
	}

	sort.Ints(coins)

	fmt.Println("denominations are:", coins)
	fmt.Println("total:", number)

	fmt.Println("ways to make change:", waysToMakeChange(number, coins))
	fmt.Println("steps", steps)
}








// The problem here is that we counted distinct orderings of coins spent,
// so if you care to spend coin in an order, there are 26000+ ordered ways to
// spend $1.00.
//
// func waysToMakeChange(total int, coins []int) int {
// 	if total == 0 {
// 		return 1
// 	}
// 	if total < 0 {
// 		return 0
// 	}
// 	var subtotal int
// 	for _, coin := range coins {
// 		subtotal += waysToMakeChange(total - coin, coins)
// 	}
// 	return subtotal
// }

// This is hard-coded with 5, 10, 25 to make it clear what the algorithm does.
//
// func waysToMakeChange(total int, _ []int) int {
// 	var count int
// 	for nickels := 0; nickels <= 20; nickels++ {
// 		for dimes := 0; dimes <= 10; dimes++ {
// 			for quarters := 0; quarters <= 4; quarters++ {
// 				subtotal := nickels * 5 + dimes * 10 + quarters * 25
// 				steps += 1
// 				if subtotal == total {
// 					count++
// 				}
// 			}
// 		}
// 	}
// 	// This prints steps=1155. Answers 29.
// 	return count
// }

// This is more efficient because it "culls" possibilities that
// exceed the total earlier.
// func waysToMakeChange(total int, coins []int) int {
// 	if len(coins) == 0 {
// 		steps++
// 		if total == 0 {
// 			return 1
// 		} else {
// 			return 0
// 		}
// 	}
// 	coin := coins[0]
// 	limit := total / coin
// 	subtotal := 0
// 	for i := 0; i <= limit; i++ {
// 		subtotal += waysToMakeChange(total - i * coin, coins[1:])
// 	}
// 	// This prints steps=242 (4.7x better). Answers 29.
// 	return subtotal
// }

func gcd2(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func gcdN(a []int) int {
	if len(a) < 2 {
		return a[0]
	}
	return gcd2(a[0], gcdN(a[1:]))
}

func waysToMakeChange(total int, coins []int) int {
	// We get the same counts by dividing the GCD
	common := gcdN(append(coins, total))

	fmt.Println("GCD is", common)

	// divide the gcd from the total
	total = total / common

	// "dynamic programming" arrays, two of them
	previous := make([]int, total+1)
	current  := make([]int, total+1)

	for row := range coins {
		// this coin value
		coin := coins[row] / common

		// swap and reset the arrays
		tmp := previous
		previous = current
		current = tmp
		clear(current)
		
		// there is 1 way to make 0
		current[0] = 1

		for pos := 1; pos <= total; pos++ {
			current[pos] = previous[pos]
			if pos >= coin {
				current[pos] += current[pos-coin]
			}

			steps += 1
		}
	}

	// prints steps=60, total=29
	return current[total]
}
