# users/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError

from users.models import UserProfile


class UserProfileModelTest(TestCase):
    """Test the UserProfile model - with automatic profile creation"""

    def test_1_profile_created_automatically(self):
        """Test 1: Profile is automatically created when User is created"""
        print("\n=== Test 1: Automatic Profile Creation ===")

        # Create a user
        user = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='password123'
        )
        print(f"Created user: {user.username}")

        # Profile should exist automatically
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

        # Get the auto-created profile
        profile = UserProfile.objects.get(user=user)
        print(f"Auto-created profile for: {profile.user.username}")

        # Check default values
        self.assertEqual(profile.bio, '')
        self.assertEqual(profile.avatar_url, '')

        print("✓ Test 1 passed: Profile created automatically with empty defaults")

    def test_2_update_auto_created_profile(self):
        """Test 2: Can we update an auto-created profile?"""
        print("\n=== Test 2: Updating Auto-Created Profile ===")

        # Create user (profile auto-created)
        user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='password123'
        )

        # Get the auto-created profile
        profile = UserProfile.objects.get(user=user)

        # Update it
        profile.bio = 'I love programming!'
        profile.avatar_url = 'https://example.com/my_avatar.jpg'
        profile.save()

        # Refresh from database
        profile.refresh_from_db()

        print(f"Updated bio: {profile.bio}")
        print(f"Updated avatar: {profile.avatar_url}")

        self.assertEqual(profile.bio, 'I love programming!')
        self.assertEqual(profile.avatar_url, 'https://example.com/my_avatar.jpg')

        print("✓ Test 2 passed: Auto-created profile can be updated")

    def test_3_one_profile_per_user_enforced(self):
        """Test 3: Cannot create second profile for same user"""
        print("\n=== Test 3: One Profile Per User ===")

        # Create user (profile auto-created)
        user = User.objects.create_user(
            username='testuser3',
            email='test3@example.com',
            password='password123'
        )

        # Try to create a second profile manually
        print("Attempting to create second profile...")

        try:
            # This should fail
            UserProfile.objects.create(
                user=user,
                bio='This should fail!'
            )
            self.fail("Should have raised IntegrityError!")
        except IntegrityError as e:
            print(f"✓ Got expected IntegrityError")
            print(f"✓ Error type: {type(e).__name__}")

        print("✓ Test 3 passed: One profile per user enforced")

    def test_4_profile_string_representation(self):
        """Test 4: String representation works correctly"""
        print("\n=== Test 4: String Representation ===")

        # Create user
        user = User.objects.create_user(
            username='johnsmith',
            email='john@example.com',
            password='password123'
        )

        # Get auto-created profile
        profile = UserProfile.objects.get(user=user)

        expected_str = "johnsmith's Profile"
        actual_str = str(profile)

        print(f"Expected: {expected_str}")
        print(f"Actual: {actual_str}")

        self.assertEqual(actual_str, expected_str)
        print("✓ Test 4 passed: String representation is correct")

    def test_5_relationship_access(self):
        """Test 5: Access profile via user.profile"""
        print("\n=== Test 5: OneToOne Relationship Access ===")

        # Create user
        user = User.objects.create_user(
            username='janedoe',
            email='jane@example.com',
            password='password123'
        )

        # Access via related_name='profile'
        print(f"User: {user.username}")
        print(f"Accessing via user.profile: {user.profile}")

        # Should work
        self.assertIsNotNone(user.profile)
        self.assertEqual(user.profile.user, user)

        print("✓ Test 5 passed: Can access profile via user.profile")

    def test_6_cascade_delete(self):
        """Test 6: Profile deleted when user is deleted"""
        print("\n=== Test 6: Cascade Delete ===")

        # Create user (profile auto-created)
        user = User.objects.create_user(
            username='tobedeleted',
            email='delete@example.com',
            password='password123'
        )

        user_id = user.id
        profile_id = user.profile.id

        print(f"User ID: {user_id}")
        print(f"Profile ID: {profile_id}")
        print(f"Profile exists before delete: {UserProfile.objects.filter(id=profile_id).exists()}")

        # Delete the user
        user.delete()

        # Profile should also be deleted
        profile_exists = UserProfile.objects.filter(id=profile_id).exists()
        print(f"Profile exists after delete: {profile_exists}")

        self.assertFalse(profile_exists)
        print("✓ Test 6 passed: Profile deleted with user (CASCADE)")