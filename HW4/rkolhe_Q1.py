def cal_age(age):
	return age // 10

def cal_height(feet, inch):
	'''Converts height from feet, inch to cms'''
	return feet*30.48 + inch*2.54

def is_enzyme(enzyme):
	'''sets the value of the given enzyme wrt the equation'''
	enzyme = enzyme.lower()
	return 1 if enzyme == 'carbamazepine'or'phenytoin'or'rifampin'or'rifampicin' else 0

def get_race(race):
	'''sets the value of race params for the equation'''
	race = race.lower()
	asian = 1 if race == 'asian' else 0
	african = 1 if race == 'african' else 0
	mixed = 1 if race == 'mixed' or race == 'missing' else 0
	return (asian,african,mixed)

def is_amiodarone(amiodarone):
	'''sets value to be 1 if patient takes amioradone'''
	return 1 if amiodarone else 0

def get_gene_sum(age, height, weight, race, enzyme, amiodarone, dosage):
	'''calculates value of gene1 + gene2 acc to the given eqn'''
	asian,african,mixed = race[0],race[1],race[2]

	return dosage**0.5 - (5.6044 - 0.2614 * age + 0.0087 * height + 0.0128 * weight - 0.1092 * asian - 0.2760 * african - 0.1032 * mixed + 1.1816 * enzyme - 0.5503 * amiodarone) 

def cal_gene(gene_sum):
	'''Plugs in all possible values of both genes and finds the one which is the closest match to the gene_sum'''
	vkocr = {'VKORC1 A/G': -0.8677, 'VKORC1 A/A': -1.6974, 'VKORC1 genotype unknown': -0.4854}
	cyp2c9 = {'CYP2C9 ∗ 1/∗ 2': -0.5211, 'CYP2C9 ∗ 1/∗ 3': -0.9357, 'CYP2C9 ∗ 2/∗ 2': -1.0616, 'CYP2C9 ∗ 2/∗ 3': -1.9206, 'CYP2C9 ∗ 3/∗ 3': -2.3312, 'CYP2C9 genotype unknown': -0.2188}
	
	min_val = float('inf')
	gene_v, gene_c = '', ''
	for gene1, val1 in vkocr.items():
		for gene2, val2 in cyp2c9.items():
			if abs(val1+ val2 - gene_sum) < min_val:
				min_val = abs(val1+ val2 - gene_sum)
				gene_v, gene_c = gene1, gene2

	return gene_v, gene_c

def main():
	#set the value for input parameters
	age = cal_age(56)
	height = cal_height(5,10)
	weight = 72
	race = get_race('Caucasian')
	enzyme = is_enzyme('carbamazepine')
	amiodarone = is_amiodarone(True)
	dosage = 21

	gene_sum = get_gene_sum(age, height, weight, race, enzyme, amiodarone, dosage)
	gene_v, gene_c = cal_gene(gene_sum)

	print(f'VKORC1 gene- {gene_v}')
	print(f'CYP2C9 gene- {gene_c}')

if __name__ == '__main__':
	main()
