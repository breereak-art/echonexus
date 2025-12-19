"""
EchoWorld Community - Reddit-style social platform
Phase 1: Core social features (posts, comments, likes)
"""

import streamlit as st
from datetime import datetime
import json
from typing import List, Dict

def init_community_state():
    """Initialize community session state"""
    if "posts" not in st.session_state:
        st.session_state.posts = []
    if "user_handle" not in st.session_state:
        st.session_state.user_handle = "Anonymous Explorer"
    if "post_counter" not in st.session_state:
        st.session_state.post_counter = 0


def create_post(title: str, content: str, category: str = "General") -> Dict:
    """Create a new post"""
    st.session_state.post_counter += 1
    return {
        "id": st.session_state.post_counter,
        "title": title,
        "content": content,
        "category": category,
        "author": st.session_state.user_handle,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "likes": 0,
        "comments": [],
        "liked_by": []
    }


def add_comment_to_post(post_id: int, comment_text: str) -> bool:
    """Add a comment to a post"""
    for post in st.session_state.posts:
        if post["id"] == post_id:
            post["comments"].append({
                "author": st.session_state.user_handle,
                "text": comment_text,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "likes": 0,
                "liked_by": []
            })
            return True
    return False


def like_post(post_id: int) -> bool:
    """Like/unlike a post"""
    for post in st.session_state.posts:
        if post["id"] == post_id:
            if st.session_state.user_handle not in post["liked_by"]:
                post["liked_by"].append(st.session_state.user_handle)
                post["likes"] += 1
                return True
            else:
                post["liked_by"].remove(st.session_state.user_handle)
                post["likes"] -= 1
                return True
    return False


def like_comment(post_id: int, comment_index: int) -> bool:
    """Like/unlike a comment"""
    for post in st.session_state.posts:
        if post["id"] == post_id:
            if comment_index < len(post["comments"]):
                comment = post["comments"][comment_index]
                if st.session_state.user_handle not in comment["liked_by"]:
                    comment["liked_by"].append(st.session_state.user_handle)
                    comment["likes"] += 1
                    return True
                else:
                    comment["liked_by"].remove(st.session_state.user_handle)
                    comment["likes"] -= 1
                    return True
    return False


def get_posts_by_category(category: str = None) -> List[Dict]:
    """Get posts filtered by category"""
    if category is None or category == "All":
        return st.session_state.posts[::-1]
    return [p for p in st.session_state.posts if p["category"] == category][::-1]


def display_post(post: Dict, post_container):
    """Display a single post with comments and likes"""
    with post_container:
        # Post header
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{post['title']}**")
            st.caption(f"by {post['author']} • {post['timestamp']}")
        with col2:
            st.caption(f"📁 {post['category']}")
        with col3:
            st.caption(f"❤️ {post['likes']} likes")
        
        # Post content
        st.markdown(post['content'])
        
        # Like button
        col1, col2, col3 = st.columns([1, 3, 1])
        with col1:
            if st.button(f"❤️ Like ({post['likes']})", key=f"like_{post['id']}", use_container_width=True):
                like_post(post['id'])
                st.rerun()
        
        st.divider()
        
        # Comments section
        st.markdown(f"**Comments ({len(post['comments'])})**")
        
        if post['comments']:
            for idx, comment in enumerate(post['comments']):
                with st.container(border=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{comment['author']}**")
                        st.caption(comment['timestamp'])
                    with col2:
                        st.caption(f"❤️ {comment['likes']}")
                    
                    st.markdown(comment['text'])
                    
                    if st.button(f"❤️ Like comment", key=f"like_comment_{post['id']}_{idx}", use_container_width=False):
                        like_comment(post['id'], idx)
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
                    add_comment_to_post(post['id'], new_comment)
                    st.rerun()


def render_community_interface():
    """Main community interface"""
    init_community_state()
    
    st.header("🌍 EchoWorld Community")
    st.markdown("Share your experiences, ask questions, and learn from others relocating globally.")
    
    # User handle setter
    with st.sidebar:
        st.markdown("### Community Settings")
        st.session_state.user_handle = st.text_input(
            "Your Display Name",
            value=st.session_state.user_handle,
            placeholder="Choose a display name"
        )
    
    # Main tabs
    community_tab1, community_tab2 = st.tabs(["📰 Browse Posts", "✍️ Create Post"])
    
    with community_tab1:
        st.subheader("Community Posts")
        
        # Filter by category
        category_filter = st.selectbox(
            "Filter by category",
            ["All", "General", "Visa & Immigration", "Cost of Living", "Job Market", "Relocation Tips", "Language & Culture", "Safety & Health"]
        )
        
        posts = get_posts_by_category(category_filter)
        
        if not posts:
            st.info("No posts yet. Be the first to share your experience! 🚀")
        else:
            for post in posts:
                display_post(post, st.container())
    
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
                    new_post = create_post(post_title, post_content, post_category)
                    st.session_state.posts.append(new_post)
                    st.success("Posted! 🎉")
                    st.rerun()
        
        with col2:
            st.info("💡 Tips: Be respectful, share real experiences, and help others!")
