"""
EchoWorld Community - Reddit-style social platform
Phase 3: Edit/Delete posts and comments, Search functionality
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict
from social_db import get_community_db

def init_community_state():
    """Initialize community session state"""
    if "current_user_id" not in st.session_state:
        st.session_state.current_user_id = None
    if "edit_post_id" not in st.session_state:
        st.session_state.edit_post_id = None
    if "edit_comment_id" not in st.session_state:
        st.session_state.edit_comment_id = None

def get_current_user_id(display_name: str) -> int:
    """Get or create user in database"""
    db = get_community_db()
    return db.get_or_create_user(display_name)

def display_post(post: Dict):
    """Display a single post with comments, likes, edit, delete"""
    db = get_community_db()
    
    # Post header with edit/delete options
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"**{post['title']}**")
        st.caption(f"by {post['display_name']} • {post['created_at'].strftime('%Y-%m-%d %H:%M')}")
    with col2:
        st.caption(f"📁 {post['category']}")
    with col3:
        st.caption(f"❤️ {post['likes_count']} likes • 💬 {post['comments_count']} comments")
    
    # Post content
    st.markdown(post['content'])
    
    # Check if user owns this post
    is_author = st.session_state.current_user_id == post['user_id']
    
    # Action buttons
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col1:
        user_liked = False
        if st.session_state.current_user_id:
            user_liked = db.has_user_liked_post(st.session_state.current_user_id, post['id'])
        
        like_text = "❤️ Unlike" if user_liked else "🤍 Like"
        if st.button(f"{like_text}", key=f"like_post_{post['id']}", use_container_width=True):
            if st.session_state.current_user_id:
                db.like_post(st.session_state.current_user_id, post['id'])
                st.rerun()
            else:
                st.error("Please set your name to like posts")
    
    if is_author:
        with col2:
            if st.button("✏️ Edit", key=f"edit_post_{post['id']}", use_container_width=True):
                st.session_state.edit_post_id = post['id']
                st.rerun()
        
        with col3:
            if st.button("🗑️ Delete", key=f"delete_post_{post['id']}", use_container_width=True):
                if db.delete_post(post['id'], st.session_state.current_user_id):
                    st.success("Post deleted!")
                    st.rerun()
    
    st.divider()
    
    # Comments section
    st.markdown(f"**Comments ({post['comments_count']})**")
    
    comments = db.get_comments(post['id'])
    if comments:
        for idx, comment in enumerate(comments):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{comment['display_name']}**")
                    st.caption(comment['created_at'].strftime('%Y-%m-%d %H:%M'))
                with col2:
                    st.caption(f"❤️ {comment['likes_count']}")
                
                st.markdown(comment['content'])
                
                # Comment actions
                comment_col1, comment_col2, comment_col3 = st.columns([1, 1, 1])
                
                with comment_col1:
                    comment_user_liked = False
                    if st.session_state.current_user_id:
                        comment_user_liked = db.has_user_liked_comment(st.session_state.current_user_id, comment['id'])
                    
                    like_text = "❤️ Unlike" if comment_user_liked else "🤍 Like"
                    if st.button(f"{like_text}", key=f"like_comment_{comment['id']}", use_container_width=True):
                        if st.session_state.current_user_id:
                            db.like_comment(st.session_state.current_user_id, comment['id'])
                            st.rerun()
                
                is_comment_author = st.session_state.current_user_id == comment['user_id']
                if is_comment_author:
                    with comment_col2:
                        if st.button("✏️ Edit", key=f"edit_comment_{comment['id']}", use_container_width=True):
                            st.session_state.edit_comment_id = comment['id']
                            st.rerun()
                    
                    with comment_col3:
                        if st.button("🗑️ Delete", key=f"delete_comment_{comment['id']}", use_container_width=True):
                            if db.delete_comment(comment['id'], st.session_state.current_user_id):
                                st.success("Comment deleted!")
                                st.rerun()
    
    # Add comment
    new_comment = st.text_input(
        "Add a comment...",
        key=f"comment_input_{post['id']}",
        placeholder="Share your experience or thoughts..."
    )
    if new_comment:
        col1, col2 = st.columns([3, 1])
        with col2:
            if st.button("Post", key=f"post_comment_{post['id']}"):
                if st.session_state.current_user_id:
                    db.create_comment(post['id'], st.session_state.current_user_id, new_comment)
                    st.rerun()
                else:
                    st.error("Please set your name to comment")

def render_community_interface():
    """Main community interface with persistent database"""
    init_community_state()
    db = get_community_db()
    
    st.header("🌍 EchoWorld Community")
    st.markdown("Share your experiences, ask questions, and learn from others relocating globally.")
    
    # User handle setter in sidebar
    with st.sidebar:
        st.markdown("### Community Settings")
        display_name = st.text_input(
            "Your Display Name",
            value="",
            placeholder="Choose a display name"
        )
        
        if display_name and display_name.strip():
            if st.button("Set Name", use_container_width=True):
                st.session_state.current_user_id = get_current_user_id(display_name.strip())
                st.success(f"Welcome, {display_name}! 👋")
                st.rerun()
        
        if st.session_state.current_user_id:
            user_profile = db.get_user_profile(st.session_state.current_user_id)
            if user_profile:
                st.divider()
                st.markdown("### Your Profile")
                st.metric("Karma Points", user_profile['karma_points'])
                st.metric("Posts", user_profile['posts_count'])
                st.metric("Comments", user_profile['comments_count'])
    
    if not st.session_state.current_user_id:
        st.info("👤 Please set your display name in the sidebar to participate in the community!")
        return
    
    # Main tabs
    community_tab1, community_tab2, community_tab3 = st.tabs(["📰 Browse Posts", "✍️ Create Post", "🔍 Search"])
    
    with community_tab1:
        st.subheader("Community Posts")
        
        # Filter by category
        category_filter = st.selectbox(
            "Filter by category",
            ["All", "General", "Visa & Immigration", "Cost of Living", "Job Market", "Relocation Tips", "Language & Culture", "Safety & Health"]
        )
        
        posts = db.get_posts(category_filter)
        
        if not posts:
            st.info("No posts yet. Be the first to share your experience! 🚀")
        else:
            for post in posts:
                # Handle edit mode
                if st.session_state.edit_post_id == post['id']:
                    st.subheader("Edit Post")
                    edit_title = st.text_input("Title", value=post['title'])
                    edit_content = st.text_area("Content", value=post['content'], height=200)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("Save Changes", type="primary", use_container_width=True):
                            if db.update_post(post['id'], st.session_state.current_user_id, edit_title, edit_content):
                                st.success("Post updated!")
                                st.session_state.edit_post_id = None
                                st.rerun()
                    with col2:
                        if st.button("Cancel", use_container_width=True):
                            st.session_state.edit_post_id = None
                            st.rerun()
                else:
                    display_post(post)
                    st.divider()
    
    with community_tab2:
        st.subheader("Share Your Story")
        
        post_title = st.text_input(
            "Post Title",
            placeholder="e.g., My experience moving to Berlin from India"
        )
        
        post_category = st.selectbox(
            "Category",
            ["General", "Visa & Immigration", "Cost of Living", "Job Market", "Relocation Tips", "Language & Culture", "Safety & Health"]
        )
        
        post_content = st.text_area(
            "What's your story?",
            placeholder="Share your experience, challenges, tips, or questions about relocating...",
            height=200
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Post", type="primary", use_container_width=True):
                if not post_title:
                    st.error("Please enter a title")
                elif not post_content:
                    st.error("Please enter your story")
                else:
                    db.create_post(st.session_state.current_user_id, post_title, post_content, post_category)
                    st.success("Posted! 🎉")
                    st.rerun()
        
        with col2:
            st.info("💡 Tips: Be respectful, share real experiences, and help others!")
    
    with community_tab3:
        st.subheader("Search Posts")
        
        search_query = st.text_input(
            "Search by title or content",
            placeholder="e.g., visa, cost of living, job market..."
        )
        
        if search_query.strip():
            results = db.search_posts(search_query)
            
            if not results:
                st.info(f"No posts found matching '{search_query}'")
            else:
                st.markdown(f"**Found {len(results)} post(s)**")
                for post in results:
                    display_post(post)
                    st.divider()
        else:
            st.info("Enter a search query to find posts!")
