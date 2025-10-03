// Page Navigation
        function showPage(pageId) {
            // Hide all pages
            const pages = document.querySelectorAll('.page');
            pages.forEach(page => page.classList.add('hidden'));
            
            // Show selected page
            document.getElementById(pageId).classList.remove('hidden');
            
            // Update navigation active state
            const navButtons = document.querySelectorAll('nav button');
            navButtons.forEach(btn => btn.classList.remove('text-green-600', 'font-bold'));
            
            // Add active state to current button
            event.target.classList.add('text-green-600', 'font-bold');
        }

        // Simulate progress animations
        function animateProgress() {
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = width;
                }, 100);
            });
        }

        // Initialize animations when page loads
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(animateProgress, 500);
        });

        // Add click handlers for interactive elements
        document.addEventListener('click', function(e) {
            // Handle challenge completion
            if (e.target.textContent.includes('Mark as Complete')) {
                e.target.textContent = '✅ Completed!';
                e.target.classList.remove('bg-green-500', 'hover:bg-green-600');
                e.target.classList.add('bg-gray-400', 'cursor-not-allowed');
                
                // Show success message
                const successMsg = document.createElement('div');
                successMsg.className = 'fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-full font-bold z-50';
                successMsg.textContent = '🎉 +50 points earned!';
                document.body.appendChild(successMsg);
                
                setTimeout(() => {
                    successMsg.remove();
                }, 3000);
            }
            
            // Handle challenge acceptance
            if (e.target.textContent.includes('Accept Challenge')) {
                e.target.textContent = '✅ Accepted!';
                e.target.classList.remove('bg-blue-500', 'hover:bg-blue-600', 'bg-green-500', 'hover:bg-green-600', 'bg-purple-500', 'hover:bg-purple-600');
                e.target.classList.add('bg-gray-400', 'cursor-not-allowed');
                
                // Show success message
                const successMsg = document.createElement('div');
                successMsg.className = 'fixed top-4 right-4 bg-blue-500 text-white px-6 py-3 rounded-full font-bold z-50';
                successMsg.textContent = '🚀 Challenge accepted!';
                document.body.appendChild(successMsg);
                
                setTimeout(() => {
                    successMsg.remove();
                }, 3000);
            }
            
            // Handle approvals
            if (e.target.textContent.includes('Approve')) {
                const parentDiv = e.target.closest('.bg-yellow-50');
                if (parentDiv) {
                    parentDiv.classList.remove('bg-yellow-50', 'border-yellow-200');
                    parentDiv.classList.add('bg-green-50', 'border-green-200');
                    e.target.textContent = '✅ Approved';
                    e.target.classList.remove('bg-green-500', 'hover:bg-green-600');
                    e.target.classList.add('bg-gray-400', 'cursor-not-allowed');
                }
            }
        });

        // Add hover effects for cards
        document.addEventListener('mouseover', function(e) {
            if (e.target.classList.contains('card-hover')) {
                e.target.style.transform = 'translateY(-5px)';
            }
        });

        document.addEventListener('mouseout', function(e) {
            if (e.target.classList.contains('card-hover')) {
                e.target.style.transform = 'translateY(0)';
            }
        });