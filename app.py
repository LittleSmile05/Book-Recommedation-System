from flask import Flask, render_template, request, session, jsonify
import pickle
import numpy as np

# Load models and data
pbr_df = pickle.load(open('PopularBookRecommendation.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
book = pickle.load(open('book.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(pbr_df['Book-Title'].values),
                           author=list(pbr_df['Book-Author'].values),
                           publisher=list(pbr_df['Publisher'].values),
                           image=list(pbr_df['Image-URL-M'].values),
                           votes=list(pbr_df['Num_rating'].values),
                           rating=list(pbr_df['Avg_rating'].values))

@app.route('/recommendation')
def recommendation_ui():
    return render_template('recommendation.html')

@app.route('/recommend_books', methods=['POST'])
def recommendation():
    user_input = request.form.get('user_input', '').strip()  # Safe get + trim
    
    if not user_input:
        return render_template('recommendation.html', error="Please enter a book name.")
    
    # Normalize input
    user_input_lower = user_input.lower()
    
    # Find match (exact or partial)
    matching_book = None
    for book_title in pt.index:
        if book_title.lower() == user_input_lower:
            matching_book = book_title
            break
    if not matching_book:
        for book_title in pt.index:
            if user_input_lower in book_title.lower():
                matching_book = book_title
                break

    # If no match
    if not matching_book:
        return render_template('recommendation.html',
                               error=f"Sorry, '{user_input}' is not found in our database. Please try another book.")
    
    # Get similar items
    index = np.where(pt.index == matching_book)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),
                           key=lambda x: x[1], reverse=True)[1:9]

    data = []
    for i in similar_items:
        temp_df = book[book['Book-Title'] == pt.index[i[0]]]
        item = [
            temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0],
            temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0],
            temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]
        ]
        data.append(item)
    
    return render_template('recommendation.html', data=data)

@app.route('/get-books')
def get_books():
    try:
        # Use pbr_df columns safely
        book_name = list(pbr_df['Book-Title'].values)
        author = list(pbr_df['Book-Author'].values)
        image = list(pbr_df['Image-URL-M'].values)
        votes = list(pbr_df['Num_rating'].values)
        rating = list(pbr_df['Avg_rating'].values)

        page = request.args.get('page', 0, type=int)
        limit = request.args.get('limit', 24, type=int)
        
        start = page * limit
        end = start + limit

        # Handle case where page exceeds length
        if start >= len(book_name):
            return jsonify({'books': []})
        
        books = [
            {
                'book_name': book_name[i],
                'author': author[i],
                'rating': rating[i],
                'votes': votes[i],
                'image': image[i]
            }
            for i in range(start, min(end, len(book_name)))
        ]
        
        return jsonify({'books': books})
    
    except Exception as e:
        # Return error message for easier debugging
        return jsonify({'error': str(e)}), 500


@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    book_data = {
        'title': request.form.get('title'),
        'author': request.form.get('author'),
        'image': request.form.get('image')
    }
    
    if 'favorites' not in session:
        session['favorites'] = []
    
    if not any(fav['title'] == book_data['title'] for fav in session['favorites']):
        session['favorites'].append(book_data)
        session.modified = True
        return jsonify({'status': 'success', 'message': 'Added to favorites!'})
    else:
        return jsonify({'status': 'info', 'message': 'Already in favorites!'})

@app.route('/remove_from_favorites', methods=['POST'])
def remove_from_favorites():
    book_title = request.form.get('title')
    
    if 'favorites' in session:
        session['favorites'] = [fav for fav in session['favorites'] if fav['title'] != book_title]
        session.modified = True
        return jsonify({'status': 'success', 'message': 'Removed from favorites!'})
    
    return jsonify({'status': 'error', 'message': 'Failed to remove!'})

@app.route('/clear_favorites', methods=['POST'])
def clear_favorites():
    session['favorites'] = []
    session.modified = True
    return jsonify({'status': 'success', 'message': 'All favorites cleared!'})

if __name__ == '__main__':
    app.run(debug=True)
