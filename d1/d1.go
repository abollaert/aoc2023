package main

import (
	"bufio"
	"fmt"
	"os"
	"unicode"
)

type CalibrationValue struct {
	index int
	value uint32
}

func parseLine(line string) []CalibrationValue {
	var calibrationValues = []CalibrationValue{}

	for i, c := range line {
		if unicode.IsNumber(c) {
			calibrationValues = append(calibrationValues, CalibrationValue{
				index: i,
				value: uint32(c - '0'),
			})
		}
	}

	return calibrationValues
}

func getCalibrationValue(line []CalibrationValue) uint32 {
	return line[0].value*10 + line[len(line)-1].value
}

func main() {
	file, _ := os.Open("input.txt")
	defer file.Close()

	scanner := bufio.NewScanner(file)

	var lines = [][]CalibrationValue{}

	for scanner.Scan() {
		lines = append(lines, parseLine(scanner.Text()))
	}

	var sum uint32 = 0

	for _, line := range lines {
		sum = sum + getCalibrationValue(line)
	}

	fmt.Printf("%d\n", sum)
}
