"""
EchoWorld Community - Reddit-style social platform
Phase 2: Persistent database storage with user profiles and karma system
"""

import streamlit as st
from datetime import datetime
from typing import List, Dict
from social_db import get_community_db

def init_community_state():
    """Initialize community session state"""
    if "current_user_id" not in st.session_state:
        st.session_state.current_user_id = None

def get_current_user_id(display_name: str) -> int:
    """Get or create user in database"""
    db = get_community_db()
    return db.get_or_create_user(display_name)

def display_post(post: Dict):
    """Display a single post with comments and likes"""
    db = get_community_db()
    
    # Post header
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
    
    # Check if user has liked this post
    user_liked = False
    if st.session_state.current_user_id:
        user_liked = db.has_user_liked_post(st.session_state.current_user_id, post['id'])
    
    # Like button
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        like_text = "❤️ Unlike" if user_liked else "🤍 Like"
        if st.button(f"{like_text} ({post['likes_count']})", key=f"like_post_{post['id']}", use_container_width=True):
            if st.session_state.current_user_id:
                db.like_post(st.session_state.current_user_id, post['id'])
                st.rerun()
            else:
                st.error("Please set your name to like posts")
    
    st.divider()
    
    # Comments section
    st.markdown(f"**Comments ({post['comments_count']})**")
    
    comments = db.get_comments(post['id'])
    if comments:
        for comment in comments:
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{comment['display_name']}**")
                    st.caption(comment['created_at'].strftime('%Y-%m-%d %H:%M'))
                with col2:
                    st.caption(f"❤️ {comment['likes_count']}")
                
                st.markdown(comment['content'])
                
                # Check if user has liked this comment
                comment_user_liked = False
                if st.session_state.current_user_id:
                    comment_user_liked = db.has_user_liked_comment(st.session_state.current_user_id, comment['id'])
                
                like_text = "❤️ Unlike" if comment_user_liked else "🤍 Like"
                if st.button(f"{like_text} comment", key=f"like_comment_{comment['id']}", use_container_width=False):
                    if st.session_state.current_user_id:
                        db.like_comment(st.session_state.current_user_id, comment['id'])
                        st.rerun()
                    else:
                        st.error("Please set your name to like comments")
    
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
    community_tab1, community_tab2 = st.tabs(["📰 Browse Posts", "✍️ Create Post"])
    
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
