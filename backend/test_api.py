"""
API Tests for GreenScore Platform
Run with: pytest test_api.py -v
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthCheck:
    """Test API health and basic endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns API info."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "GreenScore API"
        assert data["status"] == "running"
        assert "endpoints" in data


class TestScoreEndpoint:
    """Test GreenScore calculation endpoint."""
    
    def test_get_score(self):
        """Test score endpoint returns valid score."""
        response = client.get("/score")
        assert response.status_code == 200
        data = response.json()
        
        # Check required fields
        assert "score" in data
        assert "status" in data
        assert "esg" in data
        assert "breakdown" in data
        
        # Validate score range
        assert 0 <= data["score"] <= 100
        
        # Validate status
        assert data["status"] in ["low", "medium", "high"]
        
        # Validate ESG components
        esg = data["esg"]
        assert "environmental" in esg
        assert "social" in esg
        assert "governance" in esg
        
    def test_esg_breakdown(self):
        """Test ESG breakdown endpoint."""
        response = client.get("/esg-breakdown")
        assert response.status_code == 200
        data = response.json()
        
        assert "overall_score" in data
        assert "esg_scores" in data


class TestTransactionsEndpoint:
    """Test transactions endpoint."""
    
    def test_get_all_transactions(self):
        """Test getting all transactions."""
        response = client.get("/transactions")
        assert response.status_code == 200
        data = response.json()
        
        assert "count" in data
        assert "transactions" in data
        assert data["count"] > 0
        
        # Validate transaction structure
        txn = data["transactions"][0]
        assert "id" in txn
        assert "description" in txn
        assert "amount" in txn
        assert "category" in txn
        assert "eco_impact" in txn
        
    def test_filter_by_category(self):
        """Test filtering transactions by category."""
        response = client.get("/transactions?category=Transport")
        assert response.status_code == 200
        data = response.json()
        
        # All returned transactions should be Transport category
        for txn in data["transactions"]:
            assert txn["category"] == "Transport"
            
    def test_get_single_transaction(self):
        """Test getting a single transaction."""
        response = client.get("/transactions/TXN001")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == "TXN001"
        
    def test_transaction_not_found(self):
        """Test 404 for non-existent transaction."""
        response = client.get("/transactions/INVALID")
        assert response.status_code == 404


class TestInsightsEndpoint:
    """Test insights generation endpoint."""
    
    def test_get_insights(self):
        """Test insights endpoint."""
        response = client.get("/insights")
        assert response.status_code == 200
        data = response.json()
        
        assert "summary" in data
        assert "highlights" in data
        assert "recommendations" in data
        assert "esg_insights" in data
        
        # Validate recommendations have required fields
        for rec in data["recommendations"]:
            assert "priority" in rec
            assert "title" in rec
            assert "action" in rec


class TestIncentivesEndpoint:
    """Test FinTech incentives endpoint."""
    
    def test_get_incentives(self):
        """Test incentives endpoint."""
        response = client.get("/incentives")
        assert response.status_code == 200
        data = response.json()
        
        assert "green_score" in data
        assert "current_tier" in data
        assert "incentives" in data
        assert "next_tier" in data
        assert "disclaimer" in data
        
        # Validate tier structure
        tier = data["current_tier"]
        assert "tier_id" in tier
        assert "tier_name" in tier
        assert "badge" in tier
        
    def test_incentives_comparison(self):
        """Test incentives comparison endpoint."""
        response = client.get("/incentives/comparison")
        assert response.status_code == 200
        data = response.json()
        
        assert "tiers" in data
        assert len(data["tiers"]) == 5  # 5 tier levels


class TestClassifyEndpoint:
    """Test AI classification endpoint."""
    
    def test_classify_sustainable(self):
        """Test classification of sustainable transaction."""
        response = client.post("/classify", json={
            "description": "Metro Rail Monthly Pass",
            "amount": 1500
        })
        assert response.status_code == 200
        data = response.json()
        
        assert "category" in data
        assert "eco_impact" in data
        assert "reasoning" in data
        assert data["eco_impact"] > 0  # Should be positive
        
    def test_classify_harmful(self):
        """Test classification of harmful transaction."""
        response = client.post("/classify", json={
            "description": "Flight Ticket Booking",
            "amount": 7500
        })
        assert response.status_code == 200
        data = response.json()
        
        assert data["eco_impact"] < 0  # Should be negative
        
    def test_classify_neutral(self):
        """Test classification of neutral transaction."""
        response = client.post("/classify", json={
            "description": "Random purchase",
            "amount": 500
        })
        assert response.status_code == 200
        data = response.json()
        
        assert data["category"] == "Other"


class TestCategories:
    """Test categories endpoint."""
    
    def test_get_categories(self):
        """Test categories statistics endpoint."""
        response = client.get("/categories")
        assert response.status_code == 200
        data = response.json()
        
        # Should have multiple categories
        assert len(data) > 0
        
        # Each category should have stats
        for cat, stats in data.items():
            assert "count" in stats
            assert "total_amount" in stats
            assert "avg_impact" in stats


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
