.SUFFIXES:

NAME	=	pictures.csv 
FILES	=	features.csv features_test.csv categories.csv categories_truth.csv output_class_I.png output_class_II.png output_scurve.png thetas.csv
SHELL := /bin/bash

ENV	=	python3 -m venv venv
ACTIVATE	=	. venv/bin/activate
MODULES		=	pip3 install numpy flake8 pandas matplotlib seaborn opencv-python plantcv
NORMINETTE	=	 alias norminette=flake8
RIGHT	=	chmod +x Distribution.py

LIST_DIR	=	$(shell find . -not -path $(S_DIR) -not -path ./.git -mindepth 1 -maxdepth 1 -type d)
LIST_CATEGORIES	=	$(shell find $(S_DIR) -mindepth 1 -maxdepth 1 -type d)

S_DIR	=	./images

RM_FILE	= rm -f
RM_DIR	= rm -rf

$(NAME):
	touch $(NAME)
	echo -n "index" >> pictures.csv
	@index=0; \
	for dir in $(LIST_CATEGORIES); do \
		if [ -d "$$dir" ]; then \
			prefix=$$(basename "$$dir" | cut -d'.' -f1 | cut -d'_' -f1); \
			if [ "$$prefix" != "$$(basename "$$dir")" ]; then \
				echo -n ",$$index" >> pictures.csv; \
				index=$$((index + 1)); \
			fi; \
		fi; \
	done
	echo "" >> pictures.csv
	echo -n "Subcategory" >> pictures.csv
	@for dir in $(LIST_CATEGORIES); do \
		if [ -d "$$dir" ]; then \
			prefix=$$(basename "$$dir" | cut -d'.' -f1 | cut -d'_' -f1); \
			echo "Processing: $$dir -> $$prefix"; \
			if [ "$$prefix" != "$$(basename "$$dir")" ]; then \
				category=$$(basename $$dir); \
				echo -n ",$$category" >> pictures.csv; \
			else \
				echo "  Skipping $$dir (no underscore found)"; \
			fi; \
		fi; \
	done
	echo "" >> pictures.csv
	echo -n "Category" >> pictures.csv
	@for dir in $(LIST_CATEGORIES); do \
		if [ -d "$$dir" ]; then \
			prefix=$$(basename "$$dir" | cut -d'.' -f1 | cut -d'_' -f1); \
			echo "Processing: $$dir -> $$prefix"; \
			if [ "$$prefix" != "$$(basename "$$dir")" ]; then \
				mkdir -p "$$prefix"; \
				npath=$$prefix/$$(basename "$$dir"); \
				mkdir -p "$$npath/Base"; \
				cp -r "$$dir/" "$$npath/Base/" && echo "  Moved $$dir to $$npath/Base"; \
				mkdir -p "$$npath/Augmented" "$$npath/Transformed" "$$npath/Histograms" "$$npath/Histogram_subcategory"; \
				echo -n ",$$prefix" >> pictures.csv; \
			else \
				echo "  Skipping $$dir (no underscore found)"; \
			fi; \
		fi; \
	done
	echo "" >> pictures.csv
	echo -n "Count" >> pictures.csv
	@for dir in $(LIST_CATEGORIES); do \
		if [ -d "$$dir" ]; then \
			if [ "$$prefix" != "$$(basename "$$dir")" ]; then \
				count_files=$$(find "$$dir" -mindepth 1 -maxdepth 1 -type f | wc -l); \
				echo -n ",$$count_files" >> pictures.csv; \
			fi; \
		fi; \
	done
	@$(ENV)
	$(ACTIVATE)
	$(MODULES)
	@$(NORMINETTE)
	@$(RIGHT)

all	:			$(NAME)

Apple	:		
				time ./Apple.sh
Grape	:		
				time ./Grape.sh

clean	:		
				$(RM_DIR) $(LIST_DIR) $(FILES)

fclean	:		clean
				$(RM_FILE) $(NAME)

re	:			fclean all

.PHONY	:		all clean fclean re Apple Grape
