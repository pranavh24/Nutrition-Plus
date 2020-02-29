from textParser import *



THRESHOLD = 0.7

HIGH_OCCURENCE = 0.2;

LOW_OCCURENCE = 0.8; 



HIGH_TEXT = "an ingredient used A LOT"

NORMAL_TEXT = "an ingredient used not so much or little"

LOW_TEXT = "an ingredient used very little";







synonyms = {



	"sugar":["fructose","galactose","lactose","maltose","sucrose","xylose","dextrose"],

	"monosodium glutamate":["hydrolyzed protein","hydrolyzed corn and soy protein","autolyzed yeast extract","autolyzed torula yeast extract"]	



}



descriptions = {



	"high fructose corn syrup":"This sweetener, made from corn, is popular with food manufacturers because it's cheaper and sweeter than cane sugar, and it maintains moisture, while preserving freshness. This additive is extremely common in processed food and is believed to contribute to heart disease. In addition to accelerating the aging process, it also raises cholesterol and triglyceride fats in the blood, making it more prone to clotting.",

	"monosodium glutamate": "MSG is made of components naturally found in our bodies of water, sodium and glutamate, but that doesnt mean its meant to be ingested. MSG is a flavor enhancer often used in seasonings, condiments, bouillons, and snack chips. It reportedly causes headaches, seizures, nausea, tightening in the chest, and a burning sensation in the forearms and neck. MSG may also be listed as hydrolyzed soy protein or autolyzed yeast.",

	"enriched flor":"Bad for health",

	"corn syrup":"This sweetener, made from corn, is popular with food manufacturers because it's cheaper and sweeter than cane sugar, and it maintains moisture, while preserving freshness. This additive is extremely common in processed food and is believed to contribute to heart disease. In addition to accelerating the aging process, it also raises cholesterol and triglyceride fats in the blood, making it more prone to clotting.",

	"sugar":"too sweet",

}







def getConcernInfo(concern):

	return descriptions[concern]

#ingredients the string, concerns is a list of items 

def printConcerns(ingredients,concerns):

	for concern in concerns:

		match,ranking =containsIngredient(ingredients,concern); 

		if (match > THRESHOLD):

			tRank =  NORMAL_TEXT;

			if (ranking < HIGH_OCCURENCE):

				 tRank = HIGH_TEXT;

			elif (ranking > LOW_OCCURENCE):

				 tRank = LOW_TEXT;

			print(concern," was located in the ingredients as",tRank,"This ingredient is of concern because:",getConcernInfo(concern));

		

		syns = synonyms[concern] if concern in synonyms.keys() else [];

		maxTrank = "-1"

		maxScore = 2;

		for syn in syns:

			match,ranking =containsIngredient(ingredients,syn); 

			if (match > THRESHOLD):

				tRank =  NORMAL_TEXT;

				if (ranking < HIGH_OCCURENCE):

					tRank = HIGH_TEXT;

				elif (ranking > LOW_OCCURENCE):

					tRank = LOW_TEXT;

				if (ranking < maxScore):

					maxScore = ranking

					maxTrank = tRank;	

		

		print(concern," was located in the ingredients as",maxTrank,"The ingredient was found under the synonym",syn,"This ingredient is of concern because:",getConcernInfo(concern));