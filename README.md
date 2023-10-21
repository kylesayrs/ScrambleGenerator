# Scramble Generator #
This repo contains tools to create word scrambles without the user knowing the answers ahead of time.

Category word lists are generated by prompting chatgpt which are then used to generate scrambles.

The scrambles are generated in a way that stochastically minimizes the gini coeficient of the distribution of characters. This makes the scrambles easier and more fun to play

## Usage ##
```
usage: scramble.py [-h] [--category CATEGORY] [--num_words NUM_WORDS]
                   [--min_word_length MIN_WORD_LENGTH] [--num_tile_sets NUM_TILE_SETS]
                   [--category_sets_path CATEGORY_SETS_PATH] [--tile_set_path TILE_SET_PATH]
                   [--scramble_dir SCRAMBLE_DIR]

options:
  -h, --help            show this help message and exit
  --category CATEGORY   Category to create scramble for. Defaults to random category
  --num_words NUM_WORDS
                        Number of words in scramble
  --min_word_length MIN_WORD_LENGTH
                        Minimum word length of words appearing in scramble
  --num_tile_sets NUM_TILE_SETS
                        Multiplier factor for tile set distribution
  --category_sets_path CATEGORY_SETS_PATH
  --tile_set_path TILE_SET_PATH
  --scramble_dir SCRAMBLE_DIR
```
```
usage: chat.py [-h] [--category CATEGORY] [--num_iterations NUM_ITERATIONS]
               [--temperature TEMPERATURE] [--category_sets_path CATEGORY_SETS_PATH]

options:
  -h, --help            show this help message and exit
  --category CATEGORY   Category to add words to. Not specifying this will print the current sets
  --num_iterations NUM_ITERATIONS
                        Number of prompt iterations
  --temperature TEMPERATURE
                        Model temperature. Higher values yield more creative responses
  --category_sets_path CATEGORY_SETS_PATH
```

## Example ##
```bash
export OPENAI_API_KEY="yourkeyhere"
python3 chat.py --category="harry potter characters"
python3 scramble.py --category="harry potter characters"
```